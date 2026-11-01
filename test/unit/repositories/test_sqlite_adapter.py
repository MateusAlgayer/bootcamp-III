"""Testes do adaptador SQLite: centavos, erros e persistência (ADR-004, ADR-007)."""

import sqlite3
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from models.budget import Budget
from models.transaction import Transaction, TransactionType
from repositories.sqlite import (
    SQLiteBudgetRepository,
    SQLiteCategoryRepository,
    SQLiteDatabase,
    SQLiteTransactionRepository,
)
from shared.errors import ConflictError, DomainError, NotFoundError, ValidationError
from shared.period import YearMonth

JANUARY = YearMonth(year=2026, month=1)


def _expense(amount: str = "50.00", category_id: int | None = None) -> Transaction:
    return Transaction(
        kind=TransactionType.EXPENSE,
        amount=Decimal(amount),
        occurred_on=date(2026, 1, 10),
        description="Compras",
        category_id=category_id,
    )


@pytest.mark.unit
def test_database_creates_parent_directory_and_schema(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "finance.db"

    database = SQLiteDatabase(path)

    assert path.exists()
    with database.connect() as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "select name from sqlite_master where type = 'table'"
            )
        }
    assert {"categories", "transactions", "budgets"} <= tables


@pytest.mark.unit
def test_seed_categories_is_idempotent(tmp_path: Path) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")

    database.seed_categories(("Mercado", "Aluguel"))
    database.seed_categories(("Mercado",))

    categories = SQLiteCategoryRepository(database).list_all()
    assert [category.name for category in categories] == ["Aluguel", "Mercado"]


@pytest.mark.unit
def test_add_stores_amount_as_integer_cents(tmp_path: Path) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    repository = SQLiteTransactionRepository(database)

    stored = repository.add(_expense("1234.56"))
    assert stored.id is not None

    with database.connect() as connection:
        row = connection.execute(
            "select amount_cents from transactions where id = ?", (stored.id,)
        ).fetchone()
    assert row is not None
    assert row["amount_cents"] == 123456
    fetched = repository.get(stored.id)
    assert fetched is not None
    assert fetched.amount == Decimal("1234.56")


@pytest.mark.unit
def test_add_with_unknown_category_raises_not_found(tmp_path: Path) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    repository = SQLiteTransactionRepository(database)

    with pytest.raises(NotFoundError):
        repository.add(_expense(category_id=999))


@pytest.mark.unit
def test_set_category_unknown_transaction_raises_not_found(
    tmp_path: Path,
) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    repository = SQLiteTransactionRepository(database)

    with pytest.raises(NotFoundError):
        repository.set_category(999, 1)


@pytest.mark.unit
def test_add_already_persisted_transaction_raises_validation(
    tmp_path: Path,
) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    repository = SQLiteTransactionRepository(database)
    stored = repository.add(_expense())

    with pytest.raises(ValidationError):
        repository.add(stored)


@pytest.mark.unit
def test_duplicate_category_raises_conflict(tmp_path: Path) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    database.seed_categories(("Mercado",))

    with pytest.raises(ConflictError):
        with database.connect() as connection:
            connection.execute("insert into categories (name) values ('Mercado')")


@pytest.mark.unit
def test_invalid_database_path_raises_domain_error(tmp_path: Path) -> None:
    directory = tmp_path / "diretorio"
    directory.mkdir()

    with pytest.raises(DomainError) as excinfo:
        SQLiteDatabase(directory)

    assert isinstance(excinfo.value.__cause__, sqlite3.Error)


@pytest.mark.unit
def test_budget_stores_limit_as_integer_cents_and_replaces(
    tmp_path: Path,
) -> None:
    database = SQLiteDatabase(tmp_path / "finance.db")
    repository = SQLiteBudgetRepository(database)

    repository.save(Budget(period=JANUARY, limit=Decimal("1500.00")))
    repository.save(Budget(period=JANUARY, limit=Decimal("1200.00")))

    with database.connect() as connection:
        row = connection.execute(
            "select limit_cents from budgets where year = ? and month = ?",
            (JANUARY.year, JANUARY.month),
        ).fetchone()
    assert row is not None
    assert row["limit_cents"] == 120000
    assert repository.get(JANUARY) == Budget(period=JANUARY, limit=Decimal("1200.00"))
