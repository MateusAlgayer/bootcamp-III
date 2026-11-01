"""Fixtures dos testes de integração."""

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _database_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Isola o banco SQLite de cada teste de integração."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "finance.db"))
