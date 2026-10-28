"""Resumo financeiro mensal (RF-005)."""

from dataclasses import dataclass
from decimal import Decimal

from shared.errors import ValidationError
from shared.money import ZERO, ensure_decimal, quantize_money
from shared.period import YearMonth


@dataclass(frozen=True, slots=True)
class MonthlySummary:
    """Totais de receitas, despesas e saldo de um único mês de competência."""

    period: YearMonth
    income: Decimal
    expenses: Decimal
    balance: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.period, YearMonth):
            raise ValidationError("resumo mensal exige um período válido")
        income = quantize_money(ensure_decimal(self.income, field="receitas"))
        expenses = quantize_money(ensure_decimal(self.expenses, field="despesas"))
        balance = quantize_money(ensure_decimal(self.balance, field="saldo"))
        if income < ZERO or expenses < ZERO:
            raise ValidationError("totais do resumo não podem ser negativos")
        if balance != income - expenses:
            raise ValidationError(
                "saldo do resumo deve ser receitas menos despesas (RF-004)"
            )
        object.__setattr__(self, "income", income)
        object.__setattr__(self, "expenses", expenses)
        object.__setattr__(self, "balance", balance)
