from decimal import Decimal

import pytest

from shared.errors import ValidationError
from shared.money import ensure_decimal, parse_amount, quantize_money


@pytest.mark.unit
def test_quantize_money_rounds_half_up():
    assert quantize_money(Decimal("10.005")) == Decimal("10.01")


@pytest.mark.unit
def test_quantize_money_normalizes_to_two_decimal_places():
    assert quantize_money(Decimal("10")) == Decimal("10.00")


@pytest.mark.unit
def test_ensure_decimal_accepts_integer():
    assert ensure_decimal(10) == Decimal("10")


@pytest.mark.unit
def test_ensure_decimal_rejects_float():
    with pytest.raises(ValidationError, match="Decimal ou inteiro"):
        ensure_decimal(10.5)


@pytest.mark.unit
def test_ensure_decimal_rejects_bool():
    with pytest.raises(ValidationError, match="bool"):
        ensure_decimal(True)


@pytest.mark.unit
def test_ensure_decimal_rejects_non_finite():
    with pytest.raises(ValidationError, match="finito"):
        ensure_decimal(Decimal("Infinity"))


@pytest.mark.unit
def test_parse_amount_returns_exact_decimal():
    assert parse_amount(" 1500.50 ") == Decimal("1500.50")


@pytest.mark.unit
def test_parse_amount_rejects_empty_string():
    with pytest.raises(ValidationError, match="vazio"):
        parse_amount("   ")


@pytest.mark.unit
def test_parse_amount_rejects_non_numeric_text():
    with pytest.raises(ValidationError, match="decimal válido"):
        parse_amount("mil reais")


@pytest.mark.unit
def test_parse_amount_rejects_nan():
    with pytest.raises(ValidationError, match="finito"):
        parse_amount("NaN")


@pytest.mark.unit
def test_parse_amount_rejects_non_text_input():
    with pytest.raises(ValidationError, match="como texto"):
        parse_amount(1500.50)  # type: ignore[arg-type]


@pytest.mark.unit
def test_parse_amount_rejects_comma_separator():
    with pytest.raises(ValidationError, match="decimal válido"):
        parse_amount("10,50")
