"""Adaptadores SQLite dos repositórios (ADR-007)."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import replace
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import cast

from models.budget import Budget
from models.category import Category
from models.transaction import Transaction, TransactionType
from shared.errors import ConflictError, DomainError, NotFoundError, ValidationError
from shared.money import cents_to_decimal, quantize_money
from shared.period import YearMonth

_SCHEMA_PATH = Path(__file__).with_name("sqlite_schema.sql")
_TRANSACTION_SELECT = (
    "select id, kind, amount_cents, occurred_on, description, category_id "
    "from transactions"
)
_TRANSACTION_BY_ID = f"{_TRANSACTION_SELECT} where id = ?"


def _to_cents(value: Decimal) -> int:
    """Converte um decimal monetário exato para centavos inteiros."""
    return int(quantize_money(value) * Decimal(100))


def _from_cents(value: int) -> Decimal:
    """Converte centavos inteiros de volta para um decimal exato."""
    return cents_to_decimal(value)


def _to_transaction(row: sqlite3.Row) -> Transaction:
    return Transaction(
        id=row["id"],
        kind=TransactionType(row["kind"]),
        amount=_from_cents(row["amount_cents"]),
        occurred_on=date.fromisoformat(row["occurred_on"]),
        description=row["description"],
        category_id=row["category_id"],
    )


def _to_budget(row: sqlite3.Row) -> Budget:
    return Budget(
        period=YearMonth(year=row["year"], month=row["month"]),
        limit=_from_cents(row["limit_cents"]),
    )


class SQLiteDatabase:
    """Banco SQLite local com esquema criado automaticamente no primeiro acesso."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise DomainError("não foi possível criar o diretório do banco") from exc
        self._initialize()

    def _initialize(self) -> None:
        try:
            schema = _SCHEMA_PATH.read_text(encoding="utf-8")
        except OSError as exc:
            raise DomainError("esquema SQLite não encontrado") from exc
        with self.connect() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(schema)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """Abre uma conexão e reencapsula falhas técnicas (ADR-004)."""
        try:
            connection = sqlite3.connect(self._path, timeout=5.0)
        except sqlite3.Error as exc:
            raise DomainError("armazenamento indisponível") from exc
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA busy_timeout = 5000")
            yield connection
            connection.commit()
        except sqlite3.IntegrityError as exc:
            connection.rollback()
            if exc.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_FOREIGNKEY:
                raise NotFoundError("registro referenciado não existe") from exc
            if exc.sqlite_errorcode in {
                sqlite3.SQLITE_CONSTRAINT_UNIQUE,
                sqlite3.SQLITE_CONSTRAINT_PRIMARYKEY,
            }:
                raise ConflictError("registro já existe") from exc
            raise DomainError("falha ao acessar o armazenamento") from exc
        except sqlite3.Error as exc:
            connection.rollback()
            raise DomainError("armazenamento indisponível") from exc
        finally:
            connection.close()

    def seed_categories(self, names: Iterable[str]) -> None:
        """Garante a existência das categorias iniciais, sem duplicá-las."""
        with self.connect() as connection:
            connection.executemany(
                "insert or ignore into categories (name) values (?)",
                ((name,) for name in names),
            )


class SQLiteTransactionRepository:
    """Repositório de transações no banco SQLite local."""

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database

    def add(self, transaction: Transaction) -> Transaction:
        if transaction.id is not None:
            raise ValidationError("transação já persistida não pode ser inserida")
        with self._database.connect() as connection:
            cursor = connection.execute(
                "insert into transactions "
                "(kind, amount_cents, occurred_on, description, category_id) "
                "values (?, ?, ?, ?, ?)",
                (
                    transaction.kind.value,
                    _to_cents(transaction.amount),
                    transaction.occurred_on.isoformat(),
                    transaction.description,
                    transaction.category_id,
                ),
            )
            new_id = cursor.lastrowid
        return replace(transaction, id=cast(int, new_id))

    def get(self, transaction_id: int) -> Transaction | None:
        with self._database.connect() as connection:
            row = connection.execute(_TRANSACTION_BY_ID, (transaction_id,)).fetchone()
        return _to_transaction(row) if row is not None else None

    def set_category(self, transaction_id: int, category_id: int) -> Transaction:
        with self._database.connect() as connection:
            cursor = connection.execute(
                "update transactions set category_id = ? where id = ?",
                (category_id, transaction_id),
            )
            if cursor.rowcount == 0:
                raise NotFoundError(f"transação {transaction_id} não existe (RF-003)")
            row = connection.execute(_TRANSACTION_BY_ID, (transaction_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"transação {transaction_id} não existe (RF-003)")
        return _to_transaction(row)

    def list_all(self) -> tuple[Transaction, ...]:
        with self._database.connect() as connection:
            rows = connection.execute(
                f"{_TRANSACTION_SELECT} order by occurred_on, id"
            ).fetchall()
        return tuple(_to_transaction(row) for row in rows)


class SQLiteCategoryRepository:
    """Repositório de categorias no banco SQLite local."""

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database

    def get(self, category_id: int) -> Category | None:
        with self._database.connect() as connection:
            row = connection.execute(
                "select id, name from categories where id = ?", (category_id,)
            ).fetchone()
        if row is None:
            return None
        return Category(id=row["id"], name=row["name"])

    def list_all(self) -> tuple[Category, ...]:
        with self._database.connect() as connection:
            rows = connection.execute(
                "select id, name from categories order by name"
            ).fetchall()
        return tuple(Category(id=row["id"], name=row["name"]) for row in rows)


class SQLiteBudgetRepository:
    """Repositório de orçamentos no banco SQLite local."""

    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database

    def save(self, budget: Budget) -> None:
        with self._database.connect() as connection:
            connection.execute(
                "insert into budgets (year, month, limit_cents) values (?, ?, ?) "
                "on conflict(year, month) do update "
                "set limit_cents = excluded.limit_cents",
                (
                    budget.period.year,
                    budget.period.month,
                    _to_cents(budget.limit),
                ),
            )

    def get(self, period: YearMonth) -> Budget | None:
        with self._database.connect() as connection:
            row = connection.execute(
                "select year, month, limit_cents from budgets "
                "where year = ? and month = ?",
                (period.year, period.month),
            ).fetchone()
        return _to_budget(row) if row is not None else None

    def list_periods(self) -> tuple[YearMonth, ...]:
        with self._database.connect() as connection:
            rows = connection.execute(
                "select year, month from budgets order by year, month"
            ).fetchall()
        return tuple(YearMonth(year=row["year"], month=row["month"]) for row in rows)
