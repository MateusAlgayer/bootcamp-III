"""Casos de uso de registro e categorização de transações (RF-001, RF-002, RF-003)."""

from datetime import date

from models.category import Category
from models.transaction import Transaction, TransactionType
from repositories.contracts import CategoryRepository, TransactionRepository
from shared.errors import NotFoundError, ValidationError
from shared.money import InvalidMoneyValueError, Money, MoneyInput


def _to_money(value: MoneyInput) -> Money:
    """Converte o valor na fronteira do serviço, rejeitando ``float`` (RNF-FIN-001)."""
    try:
        return Money(value)
    except InvalidMoneyValueError as exc:
        raise ValidationError(
            "valor monetário deve ser decimal exato, sem float (RNF-FIN-001)"
        ) from exc


class TransactionService:
    """Registra receitas e despesas e categoriza transações existentes."""

    def __init__(
        self,
        transactions: TransactionRepository,
        categories: CategoryRepository,
    ) -> None:
        self._transactions = transactions
        self._categories = categories

    def register_income(
        self,
        amount: MoneyInput,
        occurred_on: date,
        description: str,
        category_id: int | None = None,
    ) -> Transaction:
        """Registra uma receita e a devolve persistida (RF-001)."""
        return self._register(
            TransactionType.INCOME, amount, occurred_on, description, category_id
        )

    def register_expense(
        self,
        amount: MoneyInput,
        occurred_on: date,
        description: str,
        category_id: int | None = None,
    ) -> Transaction:
        """Registra uma despesa e a devolve persistida (RF-002)."""
        return self._register(
            TransactionType.EXPENSE, amount, occurred_on, description, category_id
        )

    def categorize(self, transaction_id: int, category_id: int) -> Transaction:
        """Associa uma categoria válida a uma transação existente (RF-003).

        A categoria é validada antes da gravação para que uma entrada inválida
        nunca altere a transação; a recusa de transação inexistente vem do
        contrato do repositório.
        """
        self._require_category(category_id)
        return self._transactions.set_category(transaction_id, category_id)

    def _register(
        self,
        kind: TransactionType,
        amount: MoneyInput,
        occurred_on: date,
        description: str,
        category_id: int | None,
    ) -> Transaction:
        if category_id is not None:
            self._require_category(category_id)
        transaction = Transaction(
            kind=kind,
            amount=_to_money(amount),
            occurred_on=occurred_on,
            description=description,
            category_id=category_id,
        )
        return self._transactions.add(transaction)

    def _require_category(self, category_id: int) -> Category:
        category = self._categories.get(category_id)
        if category is None:
            raise NotFoundError(f"categoria {category_id} não existe (RF-003)")
        return category
