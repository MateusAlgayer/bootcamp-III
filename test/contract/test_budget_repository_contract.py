from decimal import Decimal

import pytest

from models.budget import Budget
from repositories.contracts import BudgetRepository
from repositories.memory import InMemoryBudgetRepository
from shared.period import YearMonth

REPOSITORY_FACTORIES = [InMemoryBudgetRepository]
REPOSITORY_IDS = ["memory"]

JANUARY = YearMonth(year=2026, month=1)
FEBRUARY = YearMonth(year=2026, month=2)
MARCH = YearMonth(year=2026, month=3)


@pytest.fixture(params=REPOSITORY_FACTORIES, ids=REPOSITORY_IDS)
def repository(request) -> BudgetRepository:
    return request.param()


@pytest.mark.contract
def test_save_then_get_returns_stored_budget(repository):
    budget = Budget(period=JANUARY, limit=Decimal("1500.00"))

    repository.save(budget)

    assert repository.get(JANUARY) == budget


@pytest.mark.contract
def test_get_unknown_period_returns_none(repository):
    assert repository.get(JANUARY) is None


@pytest.mark.contract
def test_save_replaces_budget_of_same_period(repository):
    repository.save(Budget(period=JANUARY, limit=Decimal("1000.00")))
    repository.save(Budget(period=JANUARY, limit=Decimal("1200.00")))

    current = repository.get(JANUARY)

    assert current is not None
    assert current.limit == Decimal("1200.00")
    assert repository.list_periods() == (JANUARY,)


@pytest.mark.contract
def test_list_periods_returns_chronological_order(repository):
    repository.save(Budget(period=MARCH, limit=Decimal("300.00")))
    repository.save(Budget(period=JANUARY, limit=Decimal("100.00")))
    repository.save(Budget(period=FEBRUARY, limit=Decimal("200.00")))

    assert repository.list_periods() == (JANUARY, FEBRUARY, MARCH)


@pytest.mark.contract
def test_saved_budget_preserves_decimal_limit(repository):
    repository.save(Budget(period=JANUARY, limit=Decimal("999.99")))

    stored = repository.get(JANUARY)

    assert stored is not None
    assert isinstance(stored.limit, Decimal)
    assert stored.limit == Decimal("999.99")
