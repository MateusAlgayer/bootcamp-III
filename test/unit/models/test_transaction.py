"""Testes unitários da entidade Transaction (RF-001, RF-002, RF-003)."""

from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pytest

from models.transaction import Transaction, TransactionType
from shared.errors import ValidationError

TODAY = date(2026, 1, 10)


def _make(**overrides: Any) -> Transaction:
    fields: dict[str, Any] = {
        "kind": TransactionType.INCOME,
        "amount": Decimal("100.00"),
        "occurred_on": TODAY,
        "description": "Salário",
    }
    fields.update(overrides)
    return Transaction(**fields)


@pytest.mark.unit
def test_create_income_valid_data() -> None:
    tx = _make()

    assert tx.kind is TransactionType.INCOME
    assert tx.amount == Decimal("100.00")
    assert tx.occurred_on == TODAY
    assert tx.category_id is None


@pytest.mark.unit
def test_create_expense_with_category() -> None:
    tx = _make(kind=TransactionType.EXPENSE, category_id=7)

    assert tx.kind is TransactionType.EXPENSE
    assert tx.category_id == 7


@pytest.mark.unit
def test_amount_quantized_half_up() -> None:
    assert _make(amount=Decimal("10.005")).amount == Decimal("10.01")


@pytest.mark.unit
def test_amount_accepts_minimum_cent() -> None:
    assert _make(amount=Decimal("0.01")).amount == Decimal("0.01")


@pytest.mark.unit
@pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-5.00"), Decimal("0.004")])
def test_amount_rejects_non_positive(amount: Decimal) -> None:
    with pytest.raises(ValidationError):
        _make(amount=amount)


@pytest.mark.unit
def test_amount_rejects_float() -> None:
    with pytest.raises(ValidationError):
        _make(amount=10.5)


@pytest.mark.unit
def test_kind_rejects_plain_string() -> None:
    with pytest.raises(ValidationError):
        _make(kind="INCOME")


@pytest.mark.unit
@pytest.mark.parametrize("value", ["2026-01-10", datetime(2026, 1, 10, 12, 0)])
def test_occurred_on_rejects_non_date(value: object) -> None:
    with pytest.raises(ValidationError):
        _make(occurred_on=value)


@pytest.mark.unit
def test_transaction_immutable_after_creation() -> None:
    tx = _make()

    with pytest.raises(FrozenInstanceError):
        tx.amount = Decimal("1.00")  # type: ignore[misc]


@pytest.mark.unit
def test_categorization_preserves_amount_kind_and_date() -> None:
    tx = _make(kind=TransactionType.EXPENSE, amount=Decimal("42.50"))

    categorized = replace(tx, category_id=3)

    assert categorized.category_id == 3
    assert categorized.amount == Decimal("42.50")
    assert categorized.kind is TransactionType.EXPENSE
    assert categorized.occurred_on == TODAY
