from decimal import Decimal

import pytest

from models.budget import Budget
from repositories.memory import InMemoryBudgetRepository
from services.budget_service import BudgetService
from shared.errors import NotFoundError, ValidationError
from shared.period import YearMonth

JANUARY = YearMonth(year=2026, month=1)
FEBRUARY = YearMonth(year=2026, month=2)


@pytest.fixture
def repository() -> InMemoryBudgetRepository:
    return InMemoryBudgetRepository()


@pytest.fixture
def service(repository) -> BudgetService:
    return BudgetService(repository)


@pytest.mark.unit
def test_define_stores_budget_for_period(service):
    budget = service.define(JANUARY, Decimal("1500.00"))

    assert budget.limit == Decimal("1500.00")
    assert service.find(JANUARY) == budget


@pytest.mark.unit
def test_define_replaces_existing_budget_for_same_period(service, repository):
    service.define(JANUARY, Decimal("1000.00"))
    service.define(JANUARY, Decimal("1200.00"))

    current = service.get(JANUARY)

    assert current.limit == Decimal("1200.00")
    assert repository.list_periods() == (JANUARY,)


@pytest.mark.unit
def test_define_keeps_one_budget_per_period(service):
    service.define(JANUARY, Decimal("1000.00"))
    service.define(FEBRUARY, Decimal("2000.00"))

    assert service.find(JANUARY) == Budget(period=JANUARY, limit=Decimal("1000.00"))
    assert service.find(FEBRUARY) == Budget(period=FEBRUARY, limit=Decimal("2000.00"))


@pytest.mark.unit
def test_define_rejects_zero_limit(service):
    with pytest.raises(ValidationError, match="maior que zero"):
        service.define(JANUARY, Decimal("0"))


@pytest.mark.unit
def test_find_returns_none_when_period_has_no_budget(service):
    assert service.find(JANUARY) is None


@pytest.mark.unit
def test_get_raises_when_period_has_no_budget(service):
    with pytest.raises(NotFoundError, match="01/2026"):
        service.get(JANUARY)


@pytest.mark.unit
def test_compare_with_expenses_returns_remaining_amount(service):
    service.define(JANUARY, Decimal("1000.00"))

    comparison = service.compare_with_expenses(JANUARY, Decimal("250.25"))

    assert comparison.remaining == Decimal("749.75")
    assert comparison.exceeded is False


@pytest.mark.unit
def test_compare_with_expenses_detects_exceeded_budget(service):
    service.define(JANUARY, Decimal("1000.00"))

    comparison = service.compare_with_expenses(JANUARY, Decimal("1000.01"))

    assert comparison.exceeded is True


@pytest.mark.unit
def test_compare_with_expenses_requires_budget(service):
    with pytest.raises(NotFoundError):
        service.compare_with_expenses(JANUARY, Decimal("10.00"))


@pytest.mark.unit
def test_compare_with_expenses_rejects_negative_amount(service):
    service.define(JANUARY, Decimal("1000.00"))

    with pytest.raises(ValidationError, match="não podem ser negativas"):
        service.compare_with_expenses(JANUARY, Decimal("-0.01"))
