"""Formatação de valores para exibição na interface (pt-BR)."""

from decimal import ROUND_HALF_UP, Decimal

from shared.money import quantize_money

_PERCENT_QUANTUM = Decimal("0.01")


def format_currency(value: Decimal) -> str:
    """Formata um valor monetário no padrão brasileiro (ex.: ``R$ 1.234,56``)."""
    quantized = quantize_money(value)
    formatted = f"{quantized:,.2f}"
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {formatted}"


def format_percentage(ratio: Decimal) -> str:
    """Formata uma razão entre 0 e 1 como percentual (ex.: ``23,37%``)."""
    percent = (ratio * 100).quantize(_PERCENT_QUANTUM, rounding=ROUND_HALF_UP)
    return f"{percent:.2f}".replace(".", ",") + "%"
