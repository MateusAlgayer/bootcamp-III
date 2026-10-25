from datetime import date
from decimal import Decimal

import pytest

from controllers.budget_controller import BudgetController
from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryBudgetRepository, InMemoryTransactionRepository
from services.budget_service import BudgetService
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import NotFoundError, ValidationError


def _add(
    repository: InMemoryTransactionRepository,
    kind: TransactionType,
    amount: str,
    *,
    month: int = 1,
) -> None:
    repository.add(
        Transaction(
            kind=kind,
            amount=Decimal(amount),
            occurred_on=date(2026, month, 10),
            description="movimentação de teste",
        )
    )


@pytest.fixture
def transactions() -> InMemoryTransactionRepository:
    return InMemoryTransactionRepository()


@pytest.fixture
def controller(transactions: InMemoryTransactionRepository) -> BudgetController:
    return BudgetController(
        BudgetService(InMemoryBudgetRepository()), MonthlySummaryService(transactions)
    )


@pytest.mark.unit
def test_define_budget_parses_decimal_text(controller: BudgetController) -> None:
    budget = controller.define_budget(2026, 1, "1500.50")

    assert budget.limit == Decimal("1500.50")
    assert budget.period.label() == "01/2026"


@pytest.mark.unit
def test_define_budget_accepts_decimal_value(controller: BudgetController) -> None:
    budget = controller.define_budget(2026, 1, Decimal("900"))

    assert budget.limit == Decimal("900.00")


@pytest.mark.unit
def test_define_budget_rejects_invalid_amount(controller: BudgetController) -> None:
    with pytest.raises(ValidationError, match="decimal válido"):
        controller.define_budget(2026, 1, "abc")


@pytest.mark.unit
def test_define_budget_rejects_invalid_month(controller: BudgetController) -> None:
    with pytest.raises(ValidationError, match="mês"):
        controller.define_budget(2026, 13, "100.00")


@pytest.mark.unit
def test_find_budget_returns_none_when_absent(controller: BudgetController) -> None:
    assert controller.find_budget(2026, 1) is None


@pytest.mark.unit
def test_compare_with_expenses_uses_registered_expenses_of_period(
    controller: BudgetController, transactions: InMemoryTransactionRepository
) -> None:
    controller.define_budget(2026, 1, "1000.00")
    _add(transactions, TransactionType.EXPENSE, "200.10")
    _add(transactions, TransactionType.EXPENSE, "49.90")

    comparison = controller.compare_with_expenses(2026, 1)

    assert comparison.spent == Decimal("250.00")
    assert comparison.remaining == Decimal("750.00")


@pytest.mark.unit
def test_compare_with_expenses_ignores_income_and_other_months(
    controller: BudgetController, transactions: InMemoryTransactionRepository
) -> None:
    controller.define_budget(2026, 1, "1000.00")
    _add(transactions, TransactionType.INCOME, "5000.00")
    _add(transactions, TransactionType.EXPENSE, "300.00", month=2)

    comparison = controller.compare_with_expenses(2026, 1)

    assert comparison.spent == Decimal("0.00")
    assert comparison.remaining == Decimal("1000.00")


@pytest.mark.unit
def test_compare_with_expenses_reports_exceeded_budget(
    controller: BudgetController, transactions: InMemoryTransactionRepository
) -> None:
    controller.define_budget(2026, 1, "100.00")
    _add(transactions, TransactionType.EXPENSE, "120.00")

    comparison = controller.compare_with_expenses(2026, 1)

    assert comparison.exceeded
    assert comparison.remaining == Decimal("-20.00")


@pytest.mark.unit
def test_compare_with_expenses_requires_existing_budget(
    controller: BudgetController, transactions: InMemoryTransactionRepository
) -> None:
    _add(transactions, TransactionType.EXPENSE, "10.00")

    with pytest.raises(NotFoundError):
        controller.compare_with_expenses(2026, 1)
