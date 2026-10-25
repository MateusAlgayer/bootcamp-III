"""Caso de uso de resumo financeiro mensal (RF-005)."""

from models.monthly_summary import MonthlySummary
from models.transaction import Transaction
from repositories.contracts import TransactionRepository
from services.balance_service import calculate_balance, sum_by_kind
from shared.period import YearMonth


class MonthlySummaryService:
    """Consolida receitas, despesas e saldo de um período mensal."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    def summarize(self, period: YearMonth) -> MonthlySummary:
        """Resume apenas as transações do período, sem duplicá-las (RF-005)."""
        transactions = self._transactions_for(period)
        income, expenses = sum_by_kind(transactions)
        return MonthlySummary(
            period=period,
            income=income,
            expenses=expenses,
            balance=calculate_balance(transactions),
        )

    def _transactions_for(self, period: YearMonth) -> tuple[Transaction, ...]:
        return tuple(
            transaction
            for transaction in self._repository.list_all()
            if YearMonth.from_date(transaction.occurred_on) == period
        )
