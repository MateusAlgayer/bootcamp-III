from decimal import Decimal

import pytest

from models.budget import Budget, BudgetComparison
from shared.errors import ValidationError
from shared.period import YearMonth

PERIOD = YearMonth(year=2026, month=1)


@pytest.mark.unit
def test_budget_quantizes_limit():
    budget = Budget(period=PERIOD, limit=Decimal("1500.555"))

    assert budget.limit == Decimal("1500.56")


@pytest.mark.unit
@pytest.mark.parametrize("limit", [Decimal("0"), Decimal("-0.01")])
def test_budget_rejects_non_positive_limit(limit):
    with pytest.raises(ValidationError, match="maior que zero"):
        Budget(period=PERIOD, limit=limit)


@pytest.mark.unit
def test_budget_rejects_float_limit():
    with pytest.raises(ValidationError, match="Decimal ou inteiro"):
        Budget(period=PERIOD, limit=1500.50)  # type: ignore[arg-type]


@pytest.mark.unit
def test_budget_rejects_invalid_period():
    with pytest.raises(ValidationError, match="período mensal"):
        Budget(period="2026-01", limit=Decimal("100"))  # type: ignore[arg-type]


@pytest.mark.unit
def test_comparison_computes_remaining_amount():
    comparison = BudgetComparison(
        budget=Budget(period=PERIOD, limit=Decimal("1000")),
        spent=Decimal("350.50"),
    )

    assert comparison.spent == Decimal("350.50")
    assert comparison.remaining == Decimal("649.50")
    assert comparison.exceeded is False
    assert comparison.usage_ratio == Decimal("0.3505")


@pytest.mark.unit
def test_comparison_detects_exceeded_budget():
    comparison = BudgetComparison(
        budget=Budget(period=PERIOD, limit=Decimal("1000")),
        spent=Decimal("1200"),
    )

    assert comparison.exceeded is True
    assert comparison.remaining == Decimal("-200.00")
    assert comparison.usage_ratio == Decimal("1.2000")


@pytest.mark.unit
def test_comparison_rejects_negative_spent():
    budget = Budget(period=PERIOD, limit=Decimal("1000"))

    with pytest.raises(ValidationError, match="não podem ser negativas"):
        BudgetComparison(budget=budget, spent=Decimal("-1"))
