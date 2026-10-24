"""Testes unitários do serviço de transações (RF-001, RF-002, RF-003)."""

from datetime import date, datetime
from decimal import Decimal

import pytest

from models.category import Category
from models.transaction import TransactionType
from repositories.memory import (
    InMemoryCategoryRepository,
    InMemoryTransactionRepository,
)
from services.transaction_service import TransactionService
from shared.errors import NotFoundError, ValidationError

CATEGORIES = (Category(id=1, name="Mercado"), Category(id=2, name="Aluguel"))
TODAY = date(2026, 1, 10)


@pytest.fixture
def transactions() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def service(transactions: InMemoryTransactionRepository) -> TransactionService:
    categories = InMemoryCategoryRepository(CATEGORIES)
    return TransactionService(transactions, categories)


# ---------------------------------------------------------------------- #
# RF-001 — Registrar receita
# ---------------------------------------------------------------------- #
@pytest.mark.unit
def test_register_income_stores_transaction_as_income(
    service: TransactionService,
) -> None:
    stored = service.register_income("1500.00", TODAY, "Salário")

    assert stored.kind is TransactionType.INCOME
    assert stored.amount == Decimal("1500.00")
    assert stored.occurred_on == TODAY
    assert stored.description == "Salário"
    assert stored.category_id is None


@pytest.mark.unit
def test_register_income_is_recoverable_by_repository(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_income("1500.00", TODAY, "Salário")

    assert stored.id is not None
    assert transactions.get(stored.id) == stored


@pytest.mark.unit
def test_register_income_accepts_valid_optional_category(
    service: TransactionService,
) -> None:
    stored = service.register_income("80.00", TODAY, "Reembolso", category_id=2)

    assert stored.category_id == 2


@pytest.mark.unit
def test_register_income_quantizes_amount_to_exact_cents(
    service: TransactionService,
) -> None:
    stored = service.register_income(Decimal("10.005"), TODAY, "Pix recebido")

    assert stored.amount == Decimal("10.01")
    assert isinstance(stored.amount, Decimal)


@pytest.mark.unit
@pytest.mark.parametrize("amount", ["0", "-5.00"])
def test_register_income_rejects_non_positive_amount(
    service: TransactionService,
    amount: str,
) -> None:
    with pytest.raises(ValidationError):
        service.register_income(amount, TODAY, "Salário")


@pytest.mark.unit
def test_register_income_rejects_float_amount(service: TransactionService) -> None:
    with pytest.raises(ValidationError):
        service.register_income(10.5, TODAY, "Salário")


@pytest.mark.unit
def test_register_income_rejects_invalid_date(service: TransactionService) -> None:
    with pytest.raises(ValidationError):
        service.register_income("100.00", datetime(2026, 1, 10), "Salário")


@pytest.mark.unit
def test_register_income_rejects_unknown_category(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    with pytest.raises(NotFoundError):
        service.register_income("100.00", TODAY, "Salário", category_id=999)

    assert transactions.list_all() == ()


# ---------------------------------------------------------------------- #
# RF-002 — Registrar despesa
# ---------------------------------------------------------------------- #
@pytest.mark.unit
def test_register_expense_stores_transaction_as_expense(
    service: TransactionService,
) -> None:
    stored = service.register_expense("250.90", TODAY, "Aluguel")

    assert stored.kind is TransactionType.EXPENSE
    assert stored.amount == Decimal("250.90")
    assert stored.occurred_on == TODAY
    assert stored.category_id is None


@pytest.mark.unit
def test_register_expense_is_recoverable_by_repository(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_expense("250.90", TODAY, "Aluguel", category_id=1)

    assert stored.id is not None
    assert transactions.get(stored.id) == stored


@pytest.mark.unit
@pytest.mark.parametrize("amount", ["0.00", "-0.01"])
def test_register_expense_rejects_non_positive_amount(
    service: TransactionService,
    amount: str,
) -> None:
    with pytest.raises(ValidationError):
        service.register_expense(amount, TODAY, "Aluguel")


@pytest.mark.unit
def test_register_expense_rejects_float_amount(service: TransactionService) -> None:
    with pytest.raises(ValidationError):
        service.register_expense(250.9, TODAY, "Aluguel")


@pytest.mark.unit
def test_register_expense_rejects_unknown_category(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    with pytest.raises(NotFoundError):
        service.register_expense("250.90", TODAY, "Aluguel", category_id=999)

    assert transactions.list_all() == ()


# ---------------------------------------------------------------------- #
# RF-003 — Categorizar transação
# ---------------------------------------------------------------------- #
@pytest.mark.unit
def test_categorize_associates_valid_category(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_expense("250.90", TODAY, "Aluguel")

    assert stored.id is not None
    updated = service.categorize(stored.id, 1)

    assert updated.category_id == 1
    assert transactions.get(stored.id) == updated


@pytest.mark.unit
def test_categorize_preserves_amount_kind_and_date(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_expense("42.50", TODAY, "Feira")

    assert stored.id is not None
    updated = service.categorize(stored.id, 2)

    assert updated.amount == Decimal("42.50")
    assert updated.kind is TransactionType.EXPENSE
    assert updated.occurred_on == TODAY
    assert updated.description == "Feira"
    assert transactions.get(stored.id) == updated


@pytest.mark.unit
def test_categorize_rejects_unknown_transaction(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_expense("250.90", TODAY, "Aluguel")

    with pytest.raises(NotFoundError):
        service.categorize(9999, 1)

    assert stored.id is not None
    assert transactions.get(stored.id) == stored


@pytest.mark.unit
def test_categorize_rejects_unknown_category_without_changing_transaction(
    service: TransactionService,
    transactions: InMemoryTransactionRepository,
) -> None:
    stored = service.register_expense("250.90", TODAY, "Aluguel")

    assert stored.id is not None
    with pytest.raises(NotFoundError):
        service.categorize(stored.id, 999)

    assert transactions.get(stored.id) == stored
