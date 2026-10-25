"""Controller dos fluxos RF-004 e RF-005."""

from decimal import Decimal

from models.monthly_summary import MonthlySummary
from services.balance_service import BalanceService
from services.monthly_summary_service import MonthlySummaryService
from shared.period import YearMonth


class DashboardController:
    """Traduz a seleção da UI em saldo consolidado e resumo financeiro mensal."""

    def __init__(
        self, summary_service: MonthlySummaryService, balance_service: BalanceService
    ) -> None:
        self._summary_service = summary_service
        self._balance_service = balance_service

    def consolidated_balance(self) -> Decimal:
        """Retorna o saldo de todas as transações registradas (RF-004)."""
        return self._balance_service.calculate()

    def monthly_summary(self, year: int, month: int) -> MonthlySummary:
        """Retorna o resumo do mês selecionado na interface (RF-005)."""
        return self._summary_service.summarize(YearMonth(year=year, month=month))
