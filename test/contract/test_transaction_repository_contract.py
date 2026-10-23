"""Contrato dos repositórios de transação e categoria, válido para todo adaptador."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from test.fixtures.mock_supabase import MockSupabaseClient
from typing import Callable

import pytest

from models.category import Category
from models.transaction import Transaction, TransactionType
from repositories.contracts import CategoryRepository, TransactionRepository
from repositories.memory import (
    InMemoryCategoryRepository,
    InMemoryTransactionRepository,
)
from repositories.supabase_adapter import (
    SupabaseCategoryRepository,
    SupabaseTransactionRepository,
)
from shared.errors import NotFoundError, ValidationError

CATEGORIES = (Category(id=1, name="Mercado"), Category(id=2, name="Aluguel"))


@dataclass
class Repositories:
    transactions: TransactionRepository
    categories: CategoryRepository


def _memory() -> Repositories:
    return Repositories(
        InMemoryTransactionRepository(), InMemoryCategoryRepository(CATEGORIES)
    )


def _supabase() -> Repositories:
    client = MockSupabaseClient(categories=tuple((c.id, c.name) for c in CATEGORIES))
    return Repositories(
        SupabaseTransactionRepository(client),
        SupabaseCategoryRepository(client),
    )


FACTORIES: list[Callable[[], Repositories]] = [_memory, _supabase]


@pytest.fixture(params=FACTORIES, ids=["memory", "supabase"])
def repos(request: pytest.FixtureRequest) -> Repositories:
    factory: Callable[[], Repositories] = request.param
    return factory()


def _expense(amount: str = "50.00", on: date = date(2026, 1, 10)) -> Transaction:
    return Transaction(
        kind=TransactionType.EXPENSE,
        amount=Decimal(amount),
        occurred_on=on,
        description="Compras",
    )


@pytest.mark.contract
def test_add_assigns_id_and_get_returns_transaction(repos: Repositories) -> None:
    stored = repos.transactions.add(_expense())

    assert stored.id is not None
    assert repos.transactions.get(stored.id) == stored


@pytest.mark.contract
def test_add_preserves_exact_decimal_amount(repos: Repositories) -> None:
    stored = repos.transactions.add(_expense(amount="1234.56"))
    assert stored.id is not None

    fetched = repos.transactions.get(stored.id)

    assert fetched is not None
    assert isinstance(fetched.amount, Decimal)
    assert fetched.amount == Decimal("1234.56")


@pytest.mark.contract
def test_add_rejects_already_persisted_transaction(repos: Repositories) -> None:
    stored = repos.transactions.add(_expense())

    with pytest.raises(ValidationError):
        repos.transactions.add(stored)


@pytest.mark.contract
def test_get_unknown_transaction_returns_none(repos: Repositories) -> None:
    assert repos.transactions.get(999) is None


@pytest.mark.contract
def test_set_category_preserves_amount_kind_and_date(repos: Repositories) -> None:
    stored = repos.transactions.add(_expense(amount="42.50"))
    assert stored.id is not None

    updated = repos.transactions.set_category(stored.id, 1)

    assert updated.category_id == 1
    assert updated.amount == Decimal("42.50")
    assert updated.kind is TransactionType.EXPENSE
    assert updated.occurred_on == stored.occurred_on
    assert repos.transactions.get(stored.id) == updated


@pytest.mark.contract
def test_set_category_unknown_transaction_raises_not_found(
    repos: Repositories,
) -> None:
    with pytest.raises(NotFoundError):
        repos.transactions.set_category(999, 1)


@pytest.mark.contract
def test_list_all_empty_repository_returns_empty(repos: Repositories) -> None:
    assert repos.transactions.list_all() == ()


@pytest.mark.contract
def test_list_all_orders_by_date_then_id_once_each(repos: Repositories) -> None:
    late = repos.transactions.add(_expense(on=date(2026, 3, 1)))
    early_a = repos.transactions.add(_expense(on=date(2026, 1, 1)))
    early_b = repos.transactions.add(_expense(on=date(2026, 1, 1)))

    assert repos.transactions.list_all() == (early_a, early_b, late)


@pytest.mark.contract
def test_get_category_returns_known_category(repos: Repositories) -> None:
    assert repos.categories.get(1) == Category(id=1, name="Mercado")


@pytest.mark.contract
def test_get_unknown_category_returns_none(repos: Repositories) -> None:
    assert repos.categories.get(999) is None


@pytest.mark.contract
def test_list_categories_alphabetical_order(repos: Repositories) -> None:
    assert [c.name for c in repos.categories.list_all()] == ["Aluguel", "Mercado"]
