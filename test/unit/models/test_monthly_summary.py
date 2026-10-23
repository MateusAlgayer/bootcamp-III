from decimal import Decimal

import pytest

from models.monthly_summary import MonthlySummary
from shared.errors import ValidationError
from shared.period import YearMonth

JANUARY = YearMonth(year=2026, month=1)


@pytest.mark.unit
def test_summary_quantizes_totals_to_cents():
    summary = MonthlySummary(
        period=JANUARY,
        income=Decimal("10.005"),
        expenses=Decimal("0"),
        balance=Decimal("10.005"),
    )

    assert summary.income == Decimal("10.01")
    assert summary.expenses == Decimal("0.00")
    assert summary.balance == Decimal("10.01")


@pytest.mark.unit
def test_summary_accepts_negative_balance():
    summary = MonthlySummary(
        period=JANUARY,
        income=Decimal("100.00"),
        expenses=Decimal("150.00"),
        balance=Decimal("-50.00"),
    )

    assert summary.balance == Decimal("-50.00")


@pytest.mark.unit
@pytest.mark.parametrize("field", ["income", "expenses"])
def test_summary_rejects_negative_totals(field):
    values = {
        "period": JANUARY,
        "income": Decimal("100.00"),
        "expenses": Decimal("0.00"),
        "balance": Decimal("100.00"),
    }
    values[field] = Decimal("-0.01")

    with pytest.raises(ValidationError, match="não podem ser negativos"):
        MonthlySummary(**values)


@pytest.mark.unit
def test_summary_rejects_inconsistent_balance():
    with pytest.raises(ValidationError, match="receitas menos despesas"):
        MonthlySummary(
            period=JANUARY,
            income=Decimal("100.00"),
            expenses=Decimal("20.00"),
            balance=Decimal("90.00"),
        )


@pytest.mark.unit
def test_summary_rejects_float_totals():
    with pytest.raises(ValidationError, match="Decimal ou inteiro"):
        MonthlySummary(
            period=JANUARY,
            income=100.50,  # type: ignore[arg-type]
            expenses=Decimal("0"),
            balance=Decimal("100.50"),
        )


@pytest.mark.unit
def test_summary_rejects_invalid_period():
    with pytest.raises(ValidationError, match="período válido"):
        MonthlySummary(
            period="2026-01",  # type: ignore[arg-type]
            income=Decimal("0"),
            expenses=Decimal("0"),
            balance=Decimal("0"),
        )
