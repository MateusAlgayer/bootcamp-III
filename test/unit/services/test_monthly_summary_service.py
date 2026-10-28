from datetime import date
from decimal import Decimal

import pytest

from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryTransactionRepository
from services.balance_service import calculate_balance
from services.monthly_summary_service import MonthlySummaryService
from shared.period import YearMonth

JANUARY = YearMonth(year=2026, month=1)


def _add(
    repository: InMemoryTransactionRepository,
    kind: TransactionType,
    amount: str,
    *,
    year: int = 2026,
    month: int = 1,
    day: int = 10,
) -> None:
    repository.add(
        Transaction(
            kind=kind,
            amount=Decimal(amount),
            occurred_on=date(year, month, day),
            description="movimentação de teste",
        )
    )


@pytest.fixture
def repository() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def service(repository) -> MonthlySummaryService:
    return MonthlySummaryService(repository)


@pytest.mark.unit
def test_summarize_returns_zero_totals_for_empty_month(service):
    summary = service.summarize(JANUARY)

    assert summary.income == Decimal("0.00")
    assert summary.expenses == Decimal("0.00")
    assert summary.balance == Decimal("0.00")


@pytest.mark.unit
def test_summarize_filters_transactions_by_period(service, repository):
    _add(repository, TransactionType.INCOME, "1000.00", month=1)
    _add(repository, TransactionType.EXPENSE, "250.50", month=1)
    _add(repository, TransactionType.INCOME, "500.00", month=2)

    summary = service.summarize(JANUARY)

    assert summary.income == Decimal("1000.00")
    assert summary.expenses == Decimal("250.50")
    assert summary.balance == Decimal("749.50")


@pytest.mark.unit
def test_summarize_filters_by_year_and_month(service, repository):
    _add(repository, TransactionType.INCOME, "300.00", year=2025, month=1)
    _add(repository, TransactionType.EXPENSE, "80.00", year=2026, month=1)

    summary = service.summarize(JANUARY)

    assert summary.income == Decimal("0.00")
    assert summary.expenses == Decimal("80.00")
    assert summary.balance == Decimal("-80.00")


@pytest.mark.unit
def test_summarize_computes_positive_balance(service, repository):
    _add(repository, TransactionType.INCOME, "2000.00")
    _add(repository, TransactionType.EXPENSE, "1200.00")

    assert service.summarize(JANUARY).balance == Decimal("800.00")


@pytest.mark.unit
def test_summarize_computes_negative_balance(service, repository):
    _add(repository, TransactionType.INCOME, "100.00")
    _add(repository, TransactionType.EXPENSE, "450.00")

    assert service.summarize(JANUARY).balance == Decimal("-350.00")


@pytest.mark.unit
def test_summarize_balance_is_consistent_with_rf_004(service, repository):
    _add(repository, TransactionType.INCOME, "1000.00")
    _add(repository, TransactionType.EXPENSE, "250.50")
    period_transactions = tuple(
        transaction
        for transaction in repository.list_all()
        if YearMonth.from_date(transaction.occurred_on) == JANUARY
    )

    summary = service.summarize(JANUARY)

    assert summary.balance == calculate_balance(period_transactions)
    assert summary.balance == summary.income - summary.expenses


@pytest.mark.unit
def test_summarize_preserves_exact_decimal_totals(service, repository):
    _add(repository, TransactionType.INCOME, "0.10")
    _add(repository, TransactionType.INCOME, "0.20")
    _add(repository, TransactionType.EXPENSE, "0.30")

    summary = service.summarize(JANUARY)

    assert summary.income == Decimal("0.30")
    assert summary.expenses == Decimal("0.30")
    assert summary.balance == Decimal("0.00")


@pytest.mark.unit
def test_summarize_counts_each_transaction_once(service, repository):
    _add(repository, TransactionType.INCOME, "10.00")
    _add(repository, TransactionType.INCOME, "10.00")

    assert service.summarize(JANUARY).income == Decimal("20.00")
