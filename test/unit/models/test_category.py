"""Testes unitários da entidade Category (RF-003)."""

from dataclasses import FrozenInstanceError

import pytest

from models.category import Category


@pytest.mark.unit
def test_category_immutable_after_creation() -> None:
    category = Category(id=1, name="Mercado")

    with pytest.raises(FrozenInstanceError):
        category.name = "Outro"  # type: ignore[misc]
