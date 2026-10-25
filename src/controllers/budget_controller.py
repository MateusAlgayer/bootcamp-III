"""Controller do fluxo RF-006."""

from decimal import Decimal

from models.budget import Budget, BudgetComparison
from services.budget_service import BudgetService
from services.monthly_summary_service import MonthlySummaryService
from shared.money import ensure_decimal, parse_amount
from shared.period import YearMonth


class BudgetController:
    """Traduz entradas da UI em chamadas ao serviço de orçamento."""

    def __init__(
        self, budget_service: BudgetService, summary_service: MonthlySummaryService
    ) -> None:
        self._budget_service = budget_service
        self._summary_service = summary_service

    def define_budget(
        self, year: int, month: int, limit: str | Decimal | int
    ) -> Budget:
        """Define o orçamento mensal a partir dos valores informados na UI."""
        period = YearMonth(year=year, month=month)
        return self._budget_service.define(
            period, self._to_decimal(limit, field="limite")
        )

    def find_budget(self, year: int, month: int) -> Budget | None:
        """Consulta o orçamento vigente do período selecionado."""
        return self._budget_service.find(YearMonth(year=year, month=month))

    def compare_with_expenses(self, year: int, month: int) -> BudgetComparison:
        """Compara as despesas registradas no período com o orçamento (RF-006).

        As despesas vêm do resumo mensal para que a comparação use exatamente o
        mesmo recorte de período do RF-005, e não um valor digitado na UI.
        """
        period = YearMonth(year=year, month=month)
        expenses = self._summary_service.summarize(period).expenses
        return self._budget_service.compare_with_expenses(period, expenses)

    def _to_decimal(self, value: str | Decimal | int, *, field: str) -> Decimal:
        if isinstance(value, str):
            return parse_amount(value, field=field)
        return ensure_decimal(value, field=field)
