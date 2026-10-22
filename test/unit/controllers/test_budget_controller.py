from decimal import Decimal

import pytest

from controllers.budget_controller import BudgetController
from repositories.memory import InMemoryBudgetRepository
from services.budget_service import BudgetService
from shared.errors import NotFoundError, ValidationError


@pytest.fixture
def controller() -> BudgetController:
    return BudgetController(BudgetService(InMemoryBudgetRepository()))


@pytest.mark.unit
def test_define_budget_parses_decimal_text(controller):
    budget = controller.define_budget(2026, 1, "1500.50")

    assert budget.limit == Decimal("1500.50")
    assert budget.period.label() == "01/2026"


@pytest.mark.unit
def test_define_budget_accepts_decimal_value(controller):
    budget = controller.define_budget(2026, 1, Decimal("900"))

    assert budget.limit == Decimal("900.00")


@pytest.mark.unit
def test_define_budget_rejects_invalid_amount(controller):
    with pytest.raises(ValidationError, match="decimal válido"):
        controller.define_budget(2026, 1, "abc")


@pytest.mark.unit
def test_define_budget_rejects_invalid_month(controller):
    with pytest.raises(ValidationError, match="mês"):
        controller.define_budget(2026, 13, "100.00")


@pytest.mark.unit
def test_find_budget_returns_none_when_absent(controller):
    assert controller.find_budget(2026, 1) is None


@pytest.mark.unit
def test_compare_with_expenses_uses_budget_of_period(controller):
    controller.define_budget(2026, 1, "1000.00")

    comparison = controller.compare_with_expenses(2026, 1, "250.00")

    assert comparison.remaining == Decimal("750.00")


@pytest.mark.unit
def test_compare_with_expenses_requires_existing_budget(controller):
    with pytest.raises(NotFoundError):
        controller.compare_with_expenses(2026, 1, "10.00")
