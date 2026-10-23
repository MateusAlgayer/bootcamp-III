"""Testes do adaptador Supabase: formato de envio e reencapsulamento (ADR-004)."""

from datetime import date
from decimal import Decimal
from test.fixtures.mock_supabase import MockSupabaseClient

import httpx
import pytest
from postgrest.exceptions import APIError

from models.transaction import Transaction, TransactionType
from repositories.supabase_adapter import (
    SupabaseCategoryRepository,
    SupabaseTransactionRepository,
)
from shared.errors import ConflictError, DomainError, NotFoundError


def _income() -> Transaction:
    return Transaction(
        kind=TransactionType.INCOME,
        amount=Decimal("0.10"),
        occurred_on=date(2026, 1, 10),
        description="Pix",
    )


@pytest.mark.unit
def test_add_sends_amount_as_text_not_float() -> None:
    client = MockSupabaseClient()

    SupabaseTransactionRepository(client).add(_income())

    sent = client.tables["transactions"][0]["amount"]
    assert sent == Decimal("0.10")


@pytest.mark.unit
def test_set_category_unknown_category_raises_not_found() -> None:
    client = MockSupabaseClient()
    repository = SupabaseTransactionRepository(client)
    stored = repository.add(_income())
    assert stored.id is not None

    with pytest.raises(NotFoundError):
        repository.set_category(stored.id, 999)


@pytest.mark.unit
def test_unique_violation_raises_conflict() -> None:
    client = MockSupabaseClient()
    client.error = APIError({"code": "23505", "message": "duplicate key"})

    with pytest.raises(ConflictError):
        SupabaseTransactionRepository(client).add(_income())


@pytest.mark.unit
def test_unexpected_api_error_raises_domain_error() -> None:
    client = MockSupabaseClient()
    client.error = APIError({"code": "42501", "message": "permission denied"})

    with pytest.raises(DomainError) as excinfo:
        SupabaseCategoryRepository(client).list_all()

    assert type(excinfo.value) is DomainError
    assert isinstance(excinfo.value.__cause__, APIError)


@pytest.mark.unit
def test_network_failure_raises_domain_error() -> None:
    client = MockSupabaseClient()
    client.error = httpx.ConnectError("sem conexão")

    with pytest.raises(DomainError) as excinfo:
        SupabaseTransactionRepository(client).list_all()

    assert type(excinfo.value) is DomainError
