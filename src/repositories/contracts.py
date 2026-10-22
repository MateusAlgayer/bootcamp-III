"""Contratos de persistência (ports) do domínio financeiro."""

from typing import Protocol, runtime_checkable

from models.budget import Budget
from shared.period import YearMonth


@runtime_checkable
class BudgetRepository(Protocol):
    """Armazena no máximo um orçamento vigente por período (RF-006)."""

    def save(self, budget: Budget) -> None:
        """Cria ou substitui o orçamento vigente do período."""

    def get(self, period: YearMonth) -> Budget | None:
        """Retorna o orçamento vigente do período, ou ``None`` se não houver."""

    def list_periods(self) -> tuple[YearMonth, ...]:
        """Lista os períodos com orçamento definido, em ordem cronológica."""
