"""Testes da composição dos repositórios SQLite da aplicação (ADR-007)."""

from pathlib import Path

import pytest

from views.repositories import (
    DEFAULT_CATEGORY_NAMES,
    DEFAULT_DATABASE_PATH,
    build_repositories,
)


@pytest.mark.unit
def test_build_repositories_creates_database_and_seeds_categories(
    tmp_path: Path,
) -> None:
    path = tmp_path / "nested" / "finance.db"

    repositories = build_repositories(path)

    assert path.exists()
    assert [category.name for category in repositories.categories.list_all()] == sorted(
        DEFAULT_CATEGORY_NAMES
    )
    assert repositories.transactions.list_all() == ()
    assert repositories.budgets.list_periods() == ()


@pytest.mark.unit
def test_build_repositories_uses_default_path_from_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    build_repositories()

    assert (tmp_path / DEFAULT_DATABASE_PATH).exists()


@pytest.mark.unit
def test_build_repositories_seeds_categories_only_once(tmp_path: Path) -> None:
    path = tmp_path / "finance.db"

    build_repositories(path)
    repositories = build_repositories(path)

    assert len(repositories.categories.list_all()) == len(DEFAULT_CATEGORY_NAMES)
