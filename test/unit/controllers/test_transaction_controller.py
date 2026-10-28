"""Testes unitários do controller de transações (RF-001, RF-002, RF-003)."""

from datetime import date
from decimal import Decimal

import pytest

from controllers.transaction_controller import TransactionController
from models.category import Category
from models.transaction import TransactionType
from repositories.memory import (
    InMemoryCategoryRepository,
    InMemoryTransactionRepository,
)
from services.transaction_service import TransactionService
from shared.errors import NotFoundError, ValidationError

CATEGORIES = (Category(id=1, name="Mercado"),)
TODAY = date(2026, 1, 10)


@pytest.fixture
def transactions() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def controller(transactions: InMemoryTransactionRepository) -> TransactionController:
    service = TransactionService(transactions, InMemoryCategoryRepository(CATEGORIES))
    return TransactionController(service)


@pytest.mark.unit
def test_register_income_persists_ui_text_as_exact_decimal(
    controller: TransactionController,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = controller.register_income("1.234,56", TODAY, "Salário")

    assert stored.kind is TransactionType.INCOME
    assert stored.amount == Decimal("1234.56")
    assert stored.id is not None
    assert transactions.get(stored.id) == stored


@pytest.mark.unit
@pytest.mark.parametrize("amount", ["0", "-1,00", ""])
def test_register_income_rejects_invalid_amount(
    controller: TransactionController,
    transactions: InMemoryTransactionRepository,
    amount: str,
) -> None:
    with pytest.raises(ValidationError):
        controller.register_income(amount, TODAY, "Salário")

    assert transactions.list_all() == ()


@pytest.mark.unit
def test_register_expense_persists_with_optional_category(
    controller: TransactionController,
) -> None:
    stored = controller.register_expense("42,50", TODAY, "Feira", category_id=1)

    assert stored.kind is TransactionType.EXPENSE
    assert stored.amount == Decimal("42.50")
    assert stored.category_id == 1


@pytest.mark.unit
def test_register_expense_rejects_unknown_category_without_persisting(
    controller: TransactionController,
    transactions: InMemoryTransactionRepository,
) -> None:
    with pytest.raises(NotFoundError):
        controller.register_expense("42.50", TODAY, "Feira", category_id=999)

    assert transactions.list_all() == ()


@pytest.mark.unit
def test_categorize_associates_category_preserving_amount(
    controller: TransactionController,
) -> None:
    stored = controller.register_expense("42.50", TODAY, "Feira")
    assert stored.id is not None

    updated = controller.categorize(stored.id, 1)

    assert updated.category_id == 1
    assert updated.amount == Decimal("42.50")
    assert updated.kind is TransactionType.EXPENSE
    assert updated.occurred_on == TODAY


@pytest.mark.unit
def test_categorize_rejects_unknown_transaction(
    controller: TransactionController,
) -> None:
    with pytest.raises(NotFoundError):
        controller.categorize(9999, 1)


@pytest.mark.unit
def test_categorize_rejects_unknown_category(
    controller: TransactionController,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = controller.register_expense("42.50", TODAY, "Feira")
    assert stored.id is not None

    with pytest.raises(NotFoundError):
        controller.categorize(stored.id, 999)

    assert transactions.get(stored.id) == stored
