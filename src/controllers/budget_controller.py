"""Controller do fluxo RF-006."""

from decimal import Decimal

from models.budget import Budget, BudgetComparison
from services.budget_service import BudgetService
from shared.money import ensure_decimal, parse_amount
from shared.period import YearMonth


class BudgetController:
    """Traduz entradas da UI em chamadas ao serviço de orçamento."""

    def __init__(self, service: BudgetService) -> None:
        self._service = service

    def define_budget(
        self, year: int, month: int, limit: str | Decimal | int
    ) -> Budget:
        """Define o orçamento mensal a partir dos valores informados na UI."""
        period = YearMonth(year=year, month=month)
        return self._service.define(period, self._to_decimal(limit, field="limite"))

    def find_budget(self, year: int, month: int) -> Budget | None:
        """Consulta o orçamento vigente do período selecionado."""
        return self._service.find(YearMonth(year=year, month=month))

    def compare_with_expenses(
        self, year: int, month: int, spent: str | Decimal | int
    ) -> BudgetComparison:
        """Compara a despesa informada com o orçamento vigente do período."""
        period = YearMonth(year=year, month=month)
        return self._service.compare_with_expenses(
            period, self._to_decimal(spent, field="despesas")
        )

    def _to_decimal(self, value: str | Decimal | int, *, field: str) -> Decimal:
        if isinstance(value, str):
            return parse_amount(value, field=field)
        return ensure_decimal(value, field=field)
