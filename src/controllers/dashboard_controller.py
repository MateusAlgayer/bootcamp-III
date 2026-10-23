"""Controller dos fluxos RF-004 e RF-005."""

from models.monthly_summary import MonthlySummary
from services.monthly_summary_service import MonthlySummaryService
from shared.period import YearMonth


class DashboardController:
    """Traduz a seleção de período da UI em resumo financeiro mensal."""

    def __init__(self, service: MonthlySummaryService) -> None:
        self._service = service

    def monthly_summary(self, year: int, month: int) -> MonthlySummary:
        """Retorna o resumo do mês selecionado na interface."""
        return self._service.summarize(YearMonth(year=year, month=month))
