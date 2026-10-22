"""Adaptador em memória do repositório de orçamentos.

Mantém a invariante de RF-006 (no máximo um orçamento vigente por período)
enquanto a persistência SQLite descrita na ADR-001 não for implementada.
"""

from models.budget import Budget
from shared.period import YearMonth


class InMemoryBudgetRepository:
    """Repositório determinístico indexado pelo período mensal."""

    def __init__(self) -> None:
        self._budgets: dict[YearMonth, Budget] = {}

    def save(self, budget: Budget) -> None:
        self._budgets[budget.period] = budget

    def get(self, period: YearMonth) -> Budget | None:
        return self._budgets.get(period)

    def list_periods(self) -> tuple[YearMonth, ...]:
        ordered = sorted(self._budgets, key=lambda period: (period.year, period.month))
        return tuple(ordered)
