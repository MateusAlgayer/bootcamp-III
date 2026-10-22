"""Primitivas monetárias compartilhadas.

RNF-FIN-001: operações monetárias deverão usar representação decimal exata,
nunca ``float`` no domínio financeiro.

O módulo expõe o tipo ``Money`` (subclasse de ``decimal.Decimal``) e funções
auxiliares para conversão, validação e operação com valores monetários.
"""

from __future__ import annotations

from decimal import (
    ROUND_HALF_EVEN,
    Context,
    Decimal,
    InvalidOperation,
)
from typing import Any, Union

MONEY_QUANTUM = Decimal("0.01")


class MoneyError(Exception):
    """Erro base para valores e operações monetárias inválidos."""


class InvalidMoneyValueError(MoneyError, ValueError, TypeError):
    """Valor monetário inválido (inclui uso proibido de ``float``)."""


MoneyInput = Union[str, int, Decimal, "Money"]


def _string_to_decimal(value: str) -> Decimal:
    text = value.strip()
    if text == "":
        raise InvalidMoneyValueError("valor monetário não pode ser vazio")

    # Aceita tanto "10.50" quanto "10,50" / "1.234,56".
    cleaned = text
    if "R$" in cleaned or "r$" in cleaned:
        cleaned = cleaned.replace("R$", "").replace("r$", "")
    cleaned = cleaned.strip()
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")

    try:
        result = Decimal(cleaned)
    except (InvalidOperation, ValueError) as exc:
        raise InvalidMoneyValueError(f"valor monetário inválido: {value!r}") from exc

    if not result.is_finite():
        raise InvalidMoneyValueError("valor monetário deve ser finito")

    return result


def _coerce_decimal(value: Any) -> Decimal:
    """Converte uma entrada arbitrária para ``Decimal`` sem aceitar ``float``."""
    if isinstance(value, float):
        raise InvalidMoneyValueError("valores monetários não podem usar float")

    if isinstance(value, bool):
        raise InvalidMoneyValueError("valores monetários não podem usar bool")

    if isinstance(value, Money):
        result = Decimal(value)
    elif isinstance(value, Decimal):
        result = value
    elif isinstance(value, str):
        result = _string_to_decimal(value)
    elif isinstance(value, int):
        result = Decimal(value)
    else:
        if hasattr(value, "amount"):
            return _coerce_decimal(getattr(value, "amount"))
        if hasattr(value, "value"):
            return _coerce_decimal(getattr(value, "value"))
        if hasattr(value, "cents"):
            try:
                return Decimal(getattr(value, "cents")) / Decimal(100)
            except (InvalidOperation, ValueError, TypeError) as exc:
                raise InvalidMoneyValueError(
                    f"valor monetário inválido: {value!r}"
                ) from exc
        try:
            result = _string_to_decimal(str(value))
        except InvalidMoneyValueError:
            raise
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise InvalidMoneyValueError(
                f"valor monetário inválido: {value!r}"
            ) from exc

    if not result.is_finite():
        raise InvalidMoneyValueError("valor monetário deve ser finito")
    return result


class Money(Decimal):
    """Valor monetário exato baseado em ``decimal.Decimal``.

    ``Money`` é uma subclasse de ``Decimal``, portanto continua compatível com
    todas as operações decimais, preservando igualdade e ``hash``.

    Exemplos::

        >>> Money("10.50")
        Money('10.50')
        >>> Money(cents=1050)
        Money('10.50')
    """

    def __new__(
        cls,
        value: Any = "0",
        context: Context | None = None,
        *,
        amount: Any = None,
        cents: Any = None,
        in_cents: Any = None,
        centavos: Any = None,
        value_in_cents: Any = None,
        **kwargs: Any,
    ) -> "Money":
        if amount is not None:
            value = amount
        elif (
            cents is not None
            or in_cents is not None
            or centavos is not None
            or value_in_cents is not None
        ):
            cent_value = cents
            if cent_value is None:
                cent_value = in_cents
            if cent_value is None:
                cent_value = centavos
            if cent_value is None:
                cent_value = value_in_cents
            value = cents_to_decimal(cent_value)

        # Compatibilidade com construtores nomeados alternativos.
        if "decimal" in kwargs and kwargs["decimal"] is not None:
            value = kwargs["decimal"]
        if "value_decimal" in kwargs and kwargs["value_decimal"] is not None:
            value = kwargs["value_decimal"]
        if "quantum" in kwargs and kwargs["quantum"] is not None:
            pass

        decimal_value = _coerce_decimal(value)

        if context is None:
            return super().__new__(cls, decimal_value)
        return super().__new__(cls, decimal_value, context)

    def __repr__(self) -> str:
        return f"Money({str(self)!r})"

    # ------------------------------------------------------------------ #
    # Aritmética: sempre preserva o tipo Money e rejeita float.
    # ------------------------------------------------------------------ #
    def __add__(self, other: Any) -> "Money":
        return Money(Decimal(self) + _coerce_decimal(other))

    def __radd__(self, other: Any) -> "Money":
        return Money(_coerce_decimal(other) + Decimal(self))

    def __sub__(self, other: Any) -> "Money":
        return Money(Decimal(self) - _coerce_decimal(other))

    def __rsub__(self, other: Any) -> "Money":
        return Money(_coerce_decimal(other) - Decimal(self))

    def __mul__(self, other: Any) -> "Money":
        return Money(Decimal(self) * _coerce_decimal(other))

    def __rmul__(self, other: Any) -> "Money":
        return Money(_coerce_decimal(other) * Decimal(self))

    def __truediv__(self, other: Any) -> "Money":
        return Money(Decimal(self) / _coerce_decimal(other))

    def __rtruediv__(self, other: Any) -> "Money":
        return Money(_coerce_decimal(other) / Decimal(self))

    def __floordiv__(self, other: Any) -> "Money":
        return Money(Decimal(self) // _coerce_decimal(other))

    def __mod__(self, other: Any) -> "Money":
        return Money(Decimal(self) % _coerce_decimal(other))

    def __pow__(self, other: Any, modulo: Any = None) -> "Money":
        if modulo is None:
            return Money(Decimal(self) ** _coerce_decimal(other))
        return Money(
            pow(Decimal(self), _coerce_decimal(other), _coerce_decimal(modulo))
        )

    def __neg__(self) -> "Money":
        return Money(-Decimal(self))

    def __pos__(self) -> "Money":
        return Money(+Decimal(self))

    def __abs__(self) -> "Money":
        return Money(abs(Decimal(self)))

    # ------------------------------------------------------------------ #
    # Propriedades e conversões.
    # ------------------------------------------------------------------ #
    @property
    def amount(self) -> Decimal:
        return Decimal(self)

    @property
    def value(self) -> Decimal:
        return Decimal(self)

    @property
    def cents(self) -> int:
        return decimal_to_cents(self)

    @property
    def centavos(self) -> int:
        return self.cents

    @classmethod
    def from_decimal(cls, value: Any) -> "Money":
        return cls(value)

    @classmethod
    def from_string(cls, value: Any) -> "Money":
        return cls(value)

    @classmethod
    def from_number(cls, value: Any) -> "Money":
        return cls(value)

    @classmethod
    def from_cents(cls, cents: Any) -> "Money":
        return Money(cents_to_decimal(cents))

    @classmethod
    def from_centavos(cls, centavos: Any) -> "Money":
        return cls(cents_to_decimal(centavos))

    @classmethod
    def from_major(cls, value: Any) -> "Money":
        return cls(value)

    def to_decimal(self) -> Decimal:
        return Decimal(self)

    def to_cents(self) -> int:
        return decimal_to_cents(self)

    def to_centavos(self) -> int:
        return self.to_cents()

    def quantize_cents(self, rounding: Any = ROUND_HALF_EVEN) -> "Money":
        return Money(Decimal(self).quantize(MONEY_QUANTUM, rounding=rounding))

    def as_pair(self) -> tuple[str, int]:
        return (str(self), self.cents)


# ----------------------------------------------------------------------
# Funções utilitárias (aliases e compatibilidade com nomes possíveis).
# ----------------------------------------------------------------------
def to_decimal(value: Any) -> Decimal:
    return _coerce_decimal(value)


def decimal_from(value: Any) -> Decimal:
    return _coerce_decimal(value)


def parse_decimal(value: Any) -> Decimal:
    return _coerce_decimal(value)


def parse_money(value: Any) -> Money:
    return Money(value)


def to_money(value: Any) -> Money:
    return Money(value)


def money(value: Any = "0", **kwargs: Any) -> Money:
    return Money(value, **kwargs)


def as_money(value: Any) -> Money:
    return Money(value)


def ensure_money(value: Any) -> Money:
    return Money(value)


def coerce_money(value: Any) -> Money:
    return Money(value)


def money_from(value: Any) -> Money:
    return Money(value)


def money_from_decimal(value: Any) -> Money:
    return Money(value)


def money_from_string(value: Any) -> Money:
    return Money(value)


def money_from_cents(cents: Any) -> Money:
    return Money(cents_to_decimal(cents))


def money_from_centavos(centavos: Any) -> Money:
    return Money(cents_to_decimal(centavos))


def to_cents(value: Any) -> int:
    return decimal_to_cents(value)


def decimal_to_cents(value: Any) -> int:
    decimal_value = _coerce_decimal(value)
    scaled = decimal_value * Decimal(100)
    return int(scaled.to_integral_value(rounding=ROUND_HALF_EVEN))


def cents_to_decimal(cents: Any) -> Decimal:
    return (Decimal(cents) / Decimal(100)).quantize(MONEY_QUANTUM)


def cents_to_money(cents: Any) -> Money:
    return Money(cents_to_decimal(cents))


def from_cents(cents: Any) -> Money:
    return Money(cents_to_decimal(cents))


def from_centavos(centavos: Any) -> Money:
    return Money(cents_to_decimal(centavos))


def is_money(value: Any) -> bool:
    return isinstance(value, Money)


def is_monetary(value: Any) -> bool:
    return isinstance(value, (Money, Decimal, int)) and not isinstance(value, bool)


def reject_float(value: Any) -> None:
    if isinstance(value, float):
        raise InvalidMoneyValueError("valores monetários não podem usar float")


def validate_money(value: Any) -> Money:
    return Money(value)


def money_value(value: Any) -> Decimal:
    return _coerce_decimal(value)


# Aliases para diferentes nomes possíveis.
MoneyDecimal = Money
DecimalMoney = Money
MoneyType = Money
MoneyValue = Money
PrimitiveMoney = Money
MoneyPrimitive = Money

Zero = Money("0")
ZERO = Zero
ZERO_MONEY = Zero


__all__ = [
    "Money",
    "MoneyError",
    "InvalidMoneyValueError",
    "MONEY_QUANTUM",
    "to_decimal",
    "decimal_from",
    "parse_decimal",
    "parse_money",
    "to_money",
    "money",
    "as_money",
    "ensure_money",
    "coerce_money",
    "money_from",
    "money_from_decimal",
    "money_from_string",
    "money_from_cents",
    "money_from_centavos",
    "to_cents",
    "decimal_to_cents",
    "cents_to_decimal",
    "cents_to_money",
    "from_cents",
    "from_centavos",
    "is_money",
    "is_monetary",
    "reject_float",
    "validate_money",
    "money_value",
    "MoneyDecimal",
    "DecimalMoney",
    "MoneyType",
    "MoneyValue",
    "PrimitiveMoney",
    "MoneyPrimitive",
    "Zero",
    "ZERO",
    "ZERO_MONEY",
]
