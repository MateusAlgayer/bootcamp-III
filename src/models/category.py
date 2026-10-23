"""Entidade de domínio para categorias financeiras (RF-003)."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Category:
    """Categoria que pode ser associada a uma transação."""

    id: int
    name: str
