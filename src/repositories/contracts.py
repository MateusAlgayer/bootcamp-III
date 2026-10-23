"""Contratos de persistência (ports) do domínio financeiro."""

from typing import Protocol, runtime_checkable

from models.category import Category
from models.transaction import Transaction


@runtime_checkable
class TransactionRepository(Protocol):
    """Armazena transações e permite recuperá-las (RF-001, RF-002, RF-003)."""

    def add(self, transaction: Transaction) -> Transaction:
        """Persiste uma transação nova e a devolve com o ``id`` atribuído."""

    def get(self, transaction_id: int) -> Transaction | None:
        """Retorna a transação pelo ``id``, ou ``None`` se não existir."""

    def set_category(self, transaction_id: int, category_id: int) -> Transaction:
        """Associa a categoria sem alterar valor, tipo ou data (RF-003)."""

    def list_all(self) -> tuple[Transaction, ...]:
        """Lista as transações por data e ``id``, cada uma exatamente uma vez."""


@runtime_checkable
class CategoryRepository(Protocol):
    """Consulta as categorias válidas para categorização (RF-003)."""

    def get(self, category_id: int) -> Category | None:
        """Retorna a categoria pelo ``id``, ou ``None`` se não existir."""

    def list_all(self) -> tuple[Category, ...]:
        """Lista as categorias em ordem alfabética de nome."""
