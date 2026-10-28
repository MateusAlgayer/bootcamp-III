"""Entidade de domínio do orçamento mensal (RF-006)."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from shared.errors import ValidationError
from shared.money import ZERO, ensure_decimal, quantize_money
from shared.period import YearMonth


@dataclass(frozen=True, slots=True)
class Budget:
    """Orçamento de despesas vigente para um único mês de competência."""

    period: YearMonth
    limit: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.period, YearMonth):
            raise ValidationError("orçamento exige um período mensal válido")
        limit = quantize_money(ensure_decimal(self.limit, field="limite"))
        if limit <= ZERO:
            raise ValidationError(
                "limite do orçamento deve ser maior que zero (RF-006)"
            )
        object.__setattr__(self, "limit", limit)


@dataclass(frozen=True, slots=True)
class BudgetComparison:
    """Comparação entre o orçamento vigente e as despesas do período."""

    budget: Budget
    spent: Decimal

    def __post_init__(self) -> None:
        spent = quantize_money(ensure_decimal(self.spent, field="despesas"))
        if spent < ZERO:
            raise ValidationError("despesas do período não podem ser negativas")
        object.__setattr__(self, "spent", spent)

    @property
    def remaining(self) -> Decimal:
        """Saldo restante do orçamento; negativo quando houve estouro."""
        return self.budget.limit - self.spent

    @property
    def exceeded(self) -> bool:
        """Indica se as despesas ultrapassaram o orçamento vigente."""
        return self.spent > self.budget.limit

    @property
    def usage_ratio(self) -> Decimal:
        """Consumo do orçamento em relação ao limite, com quatro casas decimais."""
        ratio = self.spent / self.budget.limit
        return ratio.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
