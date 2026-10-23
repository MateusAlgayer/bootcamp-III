"""Adaptadores em memória dos repositórios, determinísticos para testes."""

from dataclasses import replace
from itertools import count

from models.category import Category
from models.transaction import Transaction
from shared.errors import NotFoundError, ValidationError


class InMemoryTransactionRepository:
    """Repositório de transações indexado por ``id`` sequencial."""

    def __init__(self) -> None:
        self._transactions: dict[int, Transaction] = {}
        self._ids = count(1)

    def add(self, transaction: Transaction) -> Transaction:
        if transaction.id is not None:
            raise ValidationError("transação já persistida não pode ser inserida")
        new_id = next(self._ids)
        stored = replace(transaction, id=new_id)
        self._transactions[new_id] = stored
        return stored

    def get(self, transaction_id: int) -> Transaction | None:
        return self._transactions.get(transaction_id)

    def set_category(self, transaction_id: int, category_id: int) -> Transaction:
        current = self._transactions.get(transaction_id)
        if current is None:
            raise NotFoundError(f"transação {transaction_id} não existe (RF-003)")
        updated = replace(current, category_id=category_id)
        self._transactions[transaction_id] = updated
        return updated

    def list_all(self) -> tuple[Transaction, ...]:
        return tuple(
            sorted(
                self._transactions.values(), key=lambda t: (t.occurred_on, t.id or 0)
            )
        )


class InMemoryCategoryRepository:
    """Repositório de categorias pré-carregado no construtor."""

    def __init__(self, categories: tuple[Category, ...] = ()) -> None:
        self._categories = {category.id: category for category in categories}

    def get(self, category_id: int) -> Category | None:
        return self._categories.get(category_id)

    def list_all(self) -> tuple[Category, ...]:
        return tuple(sorted(self._categories.values(), key=lambda c: c.name))
