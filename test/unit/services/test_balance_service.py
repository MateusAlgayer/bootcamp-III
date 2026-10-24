from datetime import date
from decimal import Decimal

import pytest

from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryTransactionRepository
from services.balance_service import (
    BalanceService,
    calculate_balance,
    sum_by_kind,
)


def _transaction(
    kind: TransactionType,
    amount: str,
    *,
    year: int = 2026,
    month: int = 1,
    day: int = 10,
) -> Transaction:
    return Transaction(
        kind=kind,
        amount=Decimal(amount),
        occurred_on=date(year, month, day),
        description="movimentação de teste",
    )


@pytest.mark.unit
def test_calculate_balance_returns_zero_without_transactions():
    assert calculate_balance(()) == Decimal("0.00")


@pytest.mark.unit
def test_balance_service_returns_zero_without_persisted_transactions():
    service = BalanceService(InMemoryTransactionRepository())

    assert service.calculate() == Decimal("0.00")


@pytest.mark.unit
def test_calculate_balance_sums_incomes():
    transactions = (
        _transaction(TransactionType.INCOME, "100.10"),
        _transaction(TransactionType.INCOME, "250.90"),
    )

    assert calculate_balance(transactions) == Decimal("351.00")


@pytest.mark.unit
def test_calculate_balance_subtracts_expenses():
    transactions = (
        _transaction(TransactionType.INCOME, "1000.00"),
        _transaction(TransactionType.EXPENSE, "350.50"),
    )

    assert calculate_balance(transactions) == Decimal("649.50")


@pytest.mark.unit
def test_calculate_balance_supports_negative_balance():
    transactions = (
        _transaction(TransactionType.INCOME, "50.00"),
        _transaction(TransactionType.EXPENSE, "200.00"),
    )

    assert calculate_balance(transactions) == Decimal("-150.00")


@pytest.mark.unit
def test_calculate_balance_preserves_exact_decimal_precision():
    transactions = (
        _transaction(TransactionType.INCOME, "0.10"),
        _transaction(TransactionType.INCOME, "0.20"),
        _transaction(TransactionType.EXPENSE, "0.30"),
    )

    assert calculate_balance(transactions) == Decimal("0.00")


@pytest.mark.unit
def test_calculate_balance_counts_each_transaction_once():
    transactions = (
        _transaction(TransactionType.INCOME, "10.00"),
        _transaction(TransactionType.INCOME, "10.00"),
        _transaction(TransactionType.EXPENSE, "5.00"),
    )

    assert calculate_balance(transactions) == Decimal("15.00")


@pytest.mark.unit
def test_balance_service_uses_all_persisted_transactions():
    repository = InMemoryTransactionRepository()
    repository.add(_transaction(TransactionType.INCOME, "1000.00", month=1))
    repository.add(_transaction(TransactionType.EXPENSE, "200.00", month=2))

    assert BalanceService(repository).calculate() == Decimal("800.00")


@pytest.mark.unit
def test_sum_by_kind_separates_income_and_expenses():
    transactions = (
        _transaction(TransactionType.INCOME, "1200.00"),
        _transaction(TransactionType.EXPENSE, "200.00"),
        _transaction(TransactionType.EXPENSE, "50.25"),
    )

    income, expenses = sum_by_kind(transactions)

    assert income == Decimal("1200.00")
    assert expenses == Decimal("250.25")
