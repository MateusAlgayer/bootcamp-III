from datetime import date

import pytest

from shared.errors import ValidationError
from shared.period import YearMonth


@pytest.mark.unit
def test_year_month_accepts_valid_period():
    period = YearMonth(year=2026, month=1)

    assert period.label() == "01/2026"


@pytest.mark.unit
def test_year_month_from_date():
    assert YearMonth.from_date(date(2026, 10, 22)) == YearMonth(year=2026, month=10)


@pytest.mark.unit
def test_year_month_is_hashable():
    periods = {YearMonth(year=2026, month=1), YearMonth(year=2026, month=1)}

    assert len(periods) == 1


@pytest.mark.unit
@pytest.mark.parametrize("month", [0, 13, -1])
def test_year_month_rejects_month_out_of_range(month):
    with pytest.raises(ValidationError, match="mês"):
        YearMonth(year=2026, month=month)


@pytest.mark.unit
@pytest.mark.parametrize("year", [0, -1, 10000])
def test_year_month_rejects_year_out_of_range(year):
    with pytest.raises(ValidationError, match="ano"):
        YearMonth(year=year, month=1)


@pytest.mark.unit
def test_year_month_rejects_bool_month():
    with pytest.raises(ValidationError, match="inteiro"):
        YearMonth(year=2026, month=True)


@pytest.mark.unit
def test_year_month_rejects_bool_year():
    with pytest.raises(ValidationError, match="inteiro"):
        YearMonth(year=True, month=1)
