"""Caso de uso de definição e acompanhamento de orçamento (RF-006)."""

from decimal import Decimal

from models.budget import Budget, BudgetComparison
from repositories.contracts import BudgetRepository
from shared.errors import NotFoundError
from shared.money import ensure_decimal, quantize_money
from shared.period import YearMonth


class BudgetService:
    """Define um orçamento por período e o compara com as despesas informadas."""

    def __init__(self, repository: BudgetRepository) -> None:
        self._repository = repository

    def define(self, period: YearMonth, limit: Decimal) -> Budget:
        """Define o orçamento do período, substituindo o vigente quando houver."""
        budget = Budget(period=period, limit=limit)
        self._repository.save(budget)
        return budget

    def find(self, period: YearMonth) -> Budget | None:
        """Retorna o orçamento vigente do período, se existir."""
        return self._repository.get(period)

    def get(self, period: YearMonth) -> Budget:
        """Retorna o orçamento vigente ou falha quando o período não tem orçamento."""
        budget = self._repository.get(period)
        if budget is None:
            raise NotFoundError(f"não há orçamento vigente para {period.label()}")
        return budget

    def compare_with_expenses(
        self, period: YearMonth, spent: Decimal
    ) -> BudgetComparison:
        """Compara as despesas do período com o orçamento vigente."""
        expenses = quantize_money(ensure_decimal(spent, field="despesas"))
        return BudgetComparison(budget=self.get(period), spent=expenses)
