"""Primitivas monetárias compartilhadas.

RNF-FIN-001: operações monetárias deverão usar representação decimal exata,
nunca ``float`` no domínio financeiro.
"""

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from shared.errors import ValidationError

MONEY_QUANTUM = Decimal("0.01")
ZERO = Decimal("0.00")


def ensure_decimal(value: object, *, field: str = "valor") -> Decimal:
    """Valida que ``value`` é um decimal exato e devolve o valor recebido."""
    if isinstance(value, bool):
        raise ValidationError(f"{field} deve ser decimal exato; bool não é aceito")
    if isinstance(value, Decimal):
        amount = value
    elif isinstance(value, int):
        amount = Decimal(value)
    else:
        raise ValidationError(
            f"{field} deve ser Decimal ou inteiro; recebido {type(value).__name__}"
        )
    if not amount.is_finite():
        raise ValidationError(f"{field} deve ser um decimal finito")
    return amount


def quantize_money(value: Decimal) -> Decimal:
    """Normaliza um valor monetário para duas casas com arredondamento explícito."""
    return ensure_decimal(value).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def parse_amount(text: str, *, field: str = "valor") -> Decimal:
    """Converte a entrada textual da borda em ``Decimal``, sem passar por ``float``."""
    if not isinstance(text, str):
        raise ValidationError(f"{field} deve ser informado como texto")
    cleaned = text.strip()
    if not cleaned:
        raise ValidationError(f"{field} não pode ser vazio")
    try:
        amount = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValidationError(f"{field} deve ser um número decimal válido") from exc
    return ensure_decimal(amount, field=field)
