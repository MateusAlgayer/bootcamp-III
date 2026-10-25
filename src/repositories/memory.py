"""Adaptadores em memória dos repositórios, determinísticos para testes."""

from dataclasses import replace
from itertools import count

from models.budget import Budget
from models.category import Category
from models.transaction import Transaction
from shared.errors import NotFoundError, ValidationError
from shared.period import YearMonth


class InMemoryTransactionRepository:
    """Repositório de transações indexado por ``id`` sequencial."""

    def __init__(self) -> None:
        self._transactions: dict[int, Transaction] = {}
        self._ids = count(1)

    def add(self, transaction: Transaction) -> Transaction:
        if transaction.id is not None:
            raise ValidationError("transação já persistida não pode ser inserida")
        new_id = next(self._ids)
        stored = replace(transaction, id=new_id)
        self._transactions[new_id] = stored
        return stored

    def get(self, transaction_id: int) -> Transaction | None:
        return self._transactions.get(transaction_id)

    def set_category(self, transaction_id: int, category_id: int) -> Transaction:
        current = self._transactions.get(transaction_id)
        if current is None:
            raise NotFoundError(f"transação {transaction_id} não existe (RF-003)")
        updated = replace(current, category_id=category_id)
        self._transactions[transaction_id] = updated
        return updated

    def list_all(self) -> tuple[Transaction, ...]:
        return tuple(
            sorted(
                self._transactions.values(), key=lambda t: (t.occurred_on, t.id or 0)
            )
        )


class InMemoryCategoryRepository:
    """Repositório de categorias pré-carregado no construtor."""

    def __init__(self, categories: tuple[Category, ...] = ()) -> None:
        self._categories = {category.id: category for category in categories}

    def get(self, category_id: int) -> Category | None:
        return self._categories.get(category_id)

    def list_all(self) -> tuple[Category, ...]:
        return tuple(sorted(self._categories.values(), key=lambda c: c.name))


class InMemoryBudgetRepository:
    """Repositório determinístico indexado pelo período mensal.

    Mantém a invariante de RF-006 (no máximo um orçamento vigente por período)
    enquanto a persistência SQLite descrita na ADR-001 não for implementada.
    """

    def __init__(self) -> None:
        self._budgets: dict[YearMonth, Budget] = {}

    def save(self, budget: Budget) -> None:
        self._budgets[budget.period] = budget

    def get(self, period: YearMonth) -> Budget | None:
        return self._budgets.get(period)

    def list_periods(self) -> tuple[YearMonth, ...]:
        ordered = sorted(self._budgets, key=lambda period: (period.year, period.month))
        return tuple(ordered)
