from datetime import date
from decimal import Decimal

import pytest

from controllers.dashboard_controller import DashboardController
from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryTransactionRepository
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import ValidationError


def _add(
    repository: InMemoryTransactionRepository,
    kind: TransactionType,
    amount: str,
    *,
    month: int = 1,
    year: int = 2026,
) -> None:
    repository.add(
        Transaction(
            kind=kind,
            amount=Decimal(amount),
            occurred_on=date(year, month, 10),
            description="movimentação de teste",
        )
    )


@pytest.fixture
def repository() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def controller(repository) -> DashboardController:
    return DashboardController(MonthlySummaryService(repository))


@pytest.mark.unit
def test_monthly_summary_returns_totals_of_selected_month(controller, repository):
    _add(repository, TransactionType.INCOME, "1000.00", month=1)
    _add(repository, TransactionType.EXPENSE, "250.00", month=1)

    summary = controller.monthly_summary(2026, 1)

    assert summary.period.label() == "01/2026"
    assert summary.income == Decimal("1000.00")
    assert summary.expenses == Decimal("250.00")
    assert summary.balance == Decimal("750.00")


@pytest.mark.unit
def test_monthly_summary_returns_zero_for_empty_month(controller):
    summary = controller.monthly_summary(2026, 2)

    assert summary.income == Decimal("0.00")
    assert summary.expenses == Decimal("0.00")
    assert summary.balance == Decimal("0.00")


@pytest.mark.unit
def test_monthly_summary_ignores_other_months(controller, repository):
    _add(repository, TransactionType.INCOME, "500.00", month=2)

    assert controller.monthly_summary(2026, 1).income == Decimal("0.00")


@pytest.mark.unit
def test_monthly_summary_rejects_invalid_month(controller):
    with pytest.raises(ValidationError, match="mês"):
        controller.monthly_summary(2026, 13)


@pytest.mark.unit
def test_monthly_summary_rejects_invalid_year(controller):
    with pytest.raises(ValidationError, match="ano"):
        controller.monthly_summary(0, 1)
