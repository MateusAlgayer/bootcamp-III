from decimal import Decimal

import pytest

from views.formatting import format_currency, format_percentage


@pytest.mark.unit
def test_format_currency_uses_brazilian_separators():
    assert format_currency(Decimal("1234.56")) == "R$ 1.234,56"


@pytest.mark.unit
def test_format_currency_formats_zero():
    assert format_currency(Decimal("0")) == "R$ 0,00"


@pytest.mark.unit
def test_format_currency_formats_negative_value():
    assert format_currency(Decimal("-150.00")) == "R$ -150,00"


@pytest.mark.unit
def test_format_currency_rounds_half_up():
    assert format_currency(Decimal("0.005")) == "R$ 0,01"
    assert format_currency(Decimal("999.995")) == "R$ 1.000,00"


@pytest.mark.unit
def test_format_percentage_uses_comma():
    assert format_percentage(Decimal("0.2337")) == "23,37%"
    assert format_percentage(Decimal("1")) == "100,00%"
