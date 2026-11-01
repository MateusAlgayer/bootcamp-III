"""Composição dos repositórios SQLite usados pelas views.

O nome do módulo não pode coincidir com o nome de um pacote de domínio
(``repositories``, ``services``, ``models``, ``shared``): o Streamlit insere
``src/views`` no início do ``sys.path``, e a colisão passaria a resolver o
módulo da view antes do pacote real.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import streamlit as st

from repositories.contracts import (
    BudgetRepository,
    CategoryRepository,
    TransactionRepository,
)
from repositories.sqlite import (
    SQLiteBudgetRepository,
    SQLiteCategoryRepository,
    SQLiteDatabase,
    SQLiteTransactionRepository,
)

DEFAULT_DATABASE_PATH = "data/finance.db"
DEFAULT_CATEGORY_NAMES: tuple[str, ...] = (
    "Alimentação",
    "Moradia",
    "Transporte",
    "Lazer",
    "Saúde",
    "Salário",
)
_SESSION_KEY = "repositories"


@dataclass(frozen=True, slots=True)
class Repositories:
    """Conjunto de repositórios compartilhado pela sessão da aplicação."""

    transactions: TransactionRepository
    categories: CategoryRepository
    budgets: BudgetRepository


def build_repositories(database_path: str | Path | None = None) -> Repositories:
    """Cria o banco SQLite e os três repositórios da aplicação."""
    path = database_path or os.environ.get("DATABASE_PATH", DEFAULT_DATABASE_PATH)
    database = SQLiteDatabase(path)
    database.seed_categories(DEFAULT_CATEGORY_NAMES)
    return Repositories(
        transactions=SQLiteTransactionRepository(database),
        categories=SQLiteCategoryRepository(database),
        budgets=SQLiteBudgetRepository(database),
    )


def get_repositories() -> Repositories:
    """Retorna os repositórios da sessão, criando-os na primeira chamada."""
    if _SESSION_KEY not in st.session_state:
        st.session_state[_SESSION_KEY] = build_repositories()
    return cast(Repositories, st.session_state[_SESSION_KEY])
