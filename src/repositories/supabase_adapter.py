"""Adaptadores Supabase (PostgREST) dos repositórios (ADR-006)."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from datetime import date
from typing import Any, cast

import httpx
from postgrest import APIResponse
from postgrest.exceptions import APIError
from supabase import Client

from models.category import Category
from models.transaction import Transaction, TransactionType
from shared.errors import ConflictError, DomainError, NotFoundError, ValidationError

# amount::text impede que o JSON do PostgREST entregue numeric como float (RNF-FIN-001).
_TRANSACTION_COLUMNS = "id,kind,amount::text,occurred_on,description,category_id"
_CATEGORY_COLUMNS = "id,name"
_UNIQUE_VIOLATION = "23505"
_FOREIGN_KEY_VIOLATION = "23503"


@contextmanager
def _storage_errors() -> Iterator[None]:
    """Reencapsula falhas técnicas do Supabase em erros de domínio (ADR-004)."""
    try:
        yield
    except APIError as exc:
        if exc.code == _FOREIGN_KEY_VIOLATION:
            raise NotFoundError("registro referenciado não existe") from exc
        if exc.code == _UNIQUE_VIOLATION:
            raise ConflictError("registro já existe") from exc
        raise DomainError("falha ao acessar o armazenamento") from exc
    except httpx.HTTPError as exc:
        raise DomainError("armazenamento indisponível") from exc


def _rows(response: APIResponse) -> list[dict[str, Any]]:
    # Consultas de tabela no PostgREST sempre devolvem uma lista de objetos JSON.
    return cast(list[dict[str, Any]], response.data)


def _to_transaction(row: dict[str, Any]) -> Transaction:
    return Transaction(
        id=row["id"],
        kind=TransactionType(row["kind"]),
        amount=row["amount"],
        occurred_on=date.fromisoformat(row["occurred_on"]),
        description=row["description"],
        category_id=row["category_id"],
    )


class SupabaseTransactionRepository:
    """Repositório de transações na tabela ``transactions`` do Supabase."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def add(self, transaction: Transaction) -> Transaction:
        if transaction.id is not None:
            raise ValidationError("transação já persistida não pode ser inserida")
        row = {
            "kind": transaction.kind.value,
            "amount": str(transaction.amount),
            "occurred_on": transaction.occurred_on.isoformat(),
            "description": transaction.description,
            "category_id": transaction.category_id,
        }
        with _storage_errors():
            response = self._client.table("transactions").insert(row).execute()
        return replace(transaction, id=_rows(response)[0]["id"])

    def get(self, transaction_id: int) -> Transaction | None:
        with _storage_errors():
            response = (
                self._client.table("transactions")
                .select(_TRANSACTION_COLUMNS)
                .eq("id", transaction_id)
                .execute()
            )
        rows = _rows(response)
        return _to_transaction(rows[0]) if rows else None

    def set_category(self, transaction_id: int, category_id: int) -> Transaction:
        with _storage_errors():
            self._client.table("transactions").update({"category_id": category_id}).eq(
                "id", transaction_id
            ).execute()
        updated = self.get(transaction_id)
        if updated is None:
            raise NotFoundError(f"transação {transaction_id} não existe (RF-003)")
        return updated

    def list_all(self) -> tuple[Transaction, ...]:
        with _storage_errors():
            response = (
                self._client.table("transactions")
                .select(_TRANSACTION_COLUMNS)
                .order("occurred_on")
                .order("id")
                .execute()
            )
        return tuple(_to_transaction(row) for row in _rows(response))


class SupabaseCategoryRepository:
    """Repositório de categorias na tabela ``categories`` do Supabase."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self, category_id: int) -> Category | None:
        with _storage_errors():
            response = (
                self._client.table("categories")
                .select(_CATEGORY_COLUMNS)
                .eq("id", category_id)
                .execute()
            )
        rows = _rows(response)
        return Category(id=rows[0]["id"], name=rows[0]["name"]) if rows else None

    def list_all(self) -> tuple[Category, ...]:
        with _storage_errors():
            response = (
                self._client.table("categories")
                .select(_CATEGORY_COLUMNS)
                .order("name")
                .execute()
            )
        return tuple(
            Category(id=row["id"], name=row["name"]) for row in _rows(response)
        )
