"""Controller dos fluxos RF-001, RF-002 e RF-003."""

from datetime import date

from models.transaction import Transaction
from services.transaction_service import TransactionService


class TransactionController:
    """Traduz entradas da UI em chamadas ao serviço de transações.

    Falhas de regra chegam à view como ``DomainError`` (ADR-004); o controller não
    as captura para que a mensagem da regra violada seja exibida sem alteração.
    """

    def __init__(self, service: TransactionService) -> None:
        self._service = service

    def register_income(
        self,
        amount: str,
        occurred_on: date,
        description: str,
        category_id: int | None = None,
    ) -> Transaction:
        """Registra a receita informada na UI (RF-001)."""
        return self._service.register_income(
            amount, occurred_on, description, category_id
        )

    def register_expense(
        self,
        amount: str,
        occurred_on: date,
        description: str,
        category_id: int | None = None,
    ) -> Transaction:
        """Registra a despesa informada na UI (RF-002)."""
        return self._service.register_expense(
            amount, occurred_on, description, category_id
        )

    def categorize(self, transaction_id: int, category_id: int) -> Transaction:
        """Associa a categoria escolhida na UI a uma transação existente (RF-003)."""
        return self._service.categorize(transaction_id, category_id)
