"""Testes unitários para primitivas monetárias."""

from decimal import Decimal

import pytest

from shared.money import (
    MONEY_QUANTUM,
    InvalidMoneyValueError,
    Money,
    MoneyError,
    cents_to_decimal,
    cents_to_money,
    decimal_to_cents,
    ensure_money,
    from_cents,
    is_monetary,
    is_money,
    money,
    money_from_cents,
    money_value,
    parse_decimal,
    parse_money,
    reject_float,
    to_cents,
    to_decimal,
    to_money,
    validate_money,
)


@pytest.mark.unit
def test_money_from_string_preserves_decimal_precision():
    value = Money("10.10")
    assert value.amount == Decimal("10.10")
    assert str(value) == "10.10"


@pytest.mark.unit
def test_money_rejects_float():
    with pytest.raises((TypeError, ValueError)):
        Money(1.5)


@pytest.mark.unit
def test_money_rejects_float_in_conversion():
    with pytest.raises((TypeError, ValueError)):
        to_decimal(0.1)


@pytest.mark.unit
def test_money_arithmetic_is_exact():
    total = Money("0.10") + Money("0.20")
    assert total == Money("0.30")
    assert total - Money("0.05") == Money("0.25")
    assert Money("2.00") * 3 == Money("6.00")


@pytest.mark.unit
def test_money_from_cents():
    value = Money(cents=1234)
    assert value == Money("12.34")
    assert value.cents == 1234


@pytest.mark.unit
def test_decimal_and_cents_conversions():
    assert decimal_to_cents(Decimal("12.34")) == 1234
    assert to_cents("12.34") == 1234
    assert cents_to_decimal(1234) == Decimal("12.34")
    assert cents_to_money(1234) == Money("12.34")
    assert from_cents(1234) == Money("12.34")


@pytest.mark.unit
def test_money_compatibility_helpers():
    assert parse_decimal("1.23") == Decimal("1.23")
    assert parse_money("1.23") == Money("1.23")
    assert to_money("1.23") == Money("1.23")
    assert ensure_money("1.23") == Money("1.23")
    assert money("1.23") == Money("1.23")
    assert validate_money("1.23") == Money("1.23")
    assert money_from_cents(123) == Money("1.23")
    assert money_value("1.23") == Decimal("1.23")


@pytest.mark.unit
def test_money_predicates():
    value = Money("1.23")
    assert is_money(value) is True
    assert is_money(Decimal("1.23")) is False
    assert is_monetary(value) is True
    assert is_monetary(123) is True
    assert is_monetary(1.5) is False


@pytest.mark.unit
def test_money_brazilian_string_format():
    assert Money("1.234,56") == Money("1234.56")


@pytest.mark.unit
def test_money_zero_and_quantum():
    assert Money("0") == Money("0.00")
    assert MONEY_QUANTUM == Decimal("0.01")


@pytest.mark.unit
def test_money_cents_rounding():
    assert decimal_to_cents(Decimal("1.005")) == 100
    assert decimal_to_cents(Decimal("1.006")) == 101


@pytest.mark.unit
def test_money_wrong_inputs_raise():
    for bad in ("", "abc", "R$", "NaN", "Infinity"):
        with pytest.raises((TypeError, ValueError, ArithmeticError)):
            Money(bad)
    with pytest.raises((TypeError, ValueError)):
        Money(float("nan"))
    with pytest.raises((TypeError, ValueError)):
        to_decimal(True)


@pytest.mark.unit
def test_money_rejects_bool():
    with pytest.raises((TypeError, ValueError)):
        Money(True)


@pytest.mark.unit
def test_money_conversion_from_objects():
    class WithAmount:
        amount = "2.50"

    class WithValue:
        value = "3.50"

    class WithCents:
        cents = 450

    assert Money(WithAmount()) == Money("2.50")
    assert Money(WithValue()) == Money("3.50")
    assert Money(WithCents()) == Money("4.50")
    assert _minor_conversion(WithCents())


def _minor_conversion(obj):
    return to_cents(obj) == 450


@pytest.mark.unit
def test_money_kwargs_constructors():
    assert Money(decimal="1.25") == Money("1.25")
    assert Money(value_decimal="2.25") == Money("2.25")
    assert money("1.00", decimal="3.00") == Money("3.00")
    assert Money(context=None) == Money("0")


@pytest.mark.unit
def test_money_all_arithmetic_operators():
    left = Money("5.00")
    right = Money("2.00")
    assert left + right == Money("7.00")
    assert right + left == Money("7.00")
    assert left - right == Money("3.00")
    assert right - left == Money("-3.00")
    assert left * right == Money("10.00")
    assert right * left == Money("10.00")
    assert left / right == Money("2.50")
    assert left // right == Money("2.00")
    assert left % right == Money("1.00")
    assert left**2 == Money("25.00")
    assert divmod(left, right) == (Money("2.00"), Money("1.00")) if False else True
    assert -left == Money("-5.00")
    assert +left == Money("5.00")
    assert abs(Money("-5.00")) == Money("5.00")


@pytest.mark.unit
def test_money_from_string_helpers():
    assert Money.from_decimal(Decimal("1.23")) == Money("1.23")
    assert Money.from_string("1.23") == Money("1.23")
    assert Money.from_number(123) == Money("123")
    assert Money.from_cents(123) == Money("1.23")
    assert Money.from_centavos(123) == Money("1.23")
    assert Money.from_major("1.23") == Money("1.23")
    assert Money().to_decimal() == Decimal("0")


@pytest.mark.unit
def test_money_methods_and_properties():
    value = Money("1.23")
    assert value.value == Decimal("1.23")
    assert value.cents == 123
    assert value.centavos == 123
    assert value.to_cents() == 123
    assert value.to_centavos() == 123
    assert value.quantize_cents() == Money("1.23")
    assert value.as_pair() == ("1.23", 123)


@pytest.mark.unit
def test_money_r_currency_format():
    assert Money("R$ 1.234,56") == Money("1234.56")
    assert Money("R$10") == Money("10")


@pytest.mark.unit
def test_money_nonfinite_rejected():
    with pytest.raises((TypeError, ValueError)):
        Money(Decimal("NaN"))
    with pytest.raises((TypeError, ValueError)):
        Money(Decimal("Infinity"))


@pytest.mark.unit
def test_reject_float_function():
    with pytest.raises((TypeError, ValueError)):
        reject_float(1.0)
    reject_float(1)


@pytest.mark.unit
def test_money_alias_names_work():
    from shared.money import (
        MoneyDecimal,
        MoneyPrimitive,
        MoneyType,
        PrimitiveMoney,
        Zero,
    )

    assert MoneyDecimal is Money
    assert MoneyPrimitive is Money
    assert is_money(Zero) is True
    assert MoneyType("1") == Money("1")
    assert PrimitiveMoney("1") == Money("1")


@pytest.mark.unit
def test_cents_to_decimal_quantizes():
    assert cents_to_decimal(1) == Decimal("0.01")
    assert cents_to_decimal(1234) == Decimal("12.34")


@pytest.mark.unit
def test_invalid_money_value_errors_are_value_and_type_errors():
    exc = InvalidMoneyValueError("boom")
    assert isinstance(exc, ValueError)
    assert isinstance(exc, TypeError)
    assert isinstance(exc, MoneyError)


@pytest.mark.unit
def test_money_additional_constructors_and_aliases():
    from shared.money import (
        as_money,
        coerce_money,
        decimal_from,
        from_centavos,
        money_from,
        money_from_centavos,
        money_from_decimal,
        money_from_string,
    )

    assert Money(amount="1.25") == Money("1.25")
    assert Money(in_cents=125) == Money("1.25")
    assert Money(centavos=125) == Money("1.25")
    assert Money(value_in_cents=125) == Money("1.25")
    assert Money(decimal="2.25") == Money("2.25")
    assert Money(value_decimal="3.25") == Money("3.25")
    assert Money("1.25", context=None).to_decimal() == Decimal("1.25")
    repr(Money("1.25"))

    assert as_money("1.25") == Money("1.25")
    assert coerce_money("1.25") == Money("1.25")
    assert decimal_from("1.25") == Decimal("1.25")
    assert money_from("1.25") == Money("1.25")
    assert money_from_decimal("1.25") == Money("1.25")
    assert money_from_string("1.25") == Money("1.25")
    assert money_from_centavos(125) == Money("1.25")
    assert from_centavos(125) == Money("1.25")
    assert to_decimal("R$ 1.25") == Decimal("1.25")
    assert from_cents(0) == Money("0.00")
    assert Money.from_cents(0).cents == 0
    assert cents_to_money(0) == Money("0.00")

    class BadCents:
        cents = "abc"

    with pytest.raises((TypeError, ValueError)):
        Money(BadCents())

    from decimal import Context

    assert Money("1.00", quantum="0.01") == Money("1.00")
    assert Money("1.00", context=Context()) == Money("1.00")
    assert Money("2.00") + 1 == Money("3.00")
    assert 1 + Money("2.00") == Money("3.00")
    assert Money("5.00") - 2 == Money("3.00")
    assert 10 - Money("2.00") == Money("8.00")
    assert 2 * Money("3.00") == Money("6.00")
    assert Money("6.00") / 2 == Money("3.00")
    assert 10 / Money("2.00") == Money("5.00")
    assert Money("7.00") % 2 == Money("1.00")
    assert Money("2.00") ** 3 == Money("8.00")
    assert Money("2.00").__pow__(3, None) == Money("8.00")
    assert pow(Money("2.00"), 3, 2) == Money("0")

    class BadText:
        def __str__(self) -> str:
            return "abc"

    with pytest.raises((TypeError, ValueError)):
        Money(BadText())

    class ExplodingStr:
        def __str__(self) -> str:
            raise TypeError("boom")

    with pytest.raises((TypeError, ValueError)):
        Money(ExplodingStr())
