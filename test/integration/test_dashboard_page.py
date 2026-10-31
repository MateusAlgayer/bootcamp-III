from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from models.transaction import Transaction, TransactionType
from views.repositories import Repositories, build_repositories

ROOT_DIR = Path(__file__).resolve().parents[2]
DASHBOARD_PAGE = ROOT_DIR / "src" / "views" / "screens" / "dashboard.py"


def _repositories_with_transactions(tmp_path: Path) -> Repositories:
    repositories = build_repositories(tmp_path / "finance.db")
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("1500.00"),
            occurred_on=date(2026, 1, 5),
            description="salário",
        )
    )
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.EXPENSE,
            amount=Decimal("500.25"),
            occurred_on=date(2026, 1, 20),
            description="aluguel",
        )
    )
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("300.00"),
            occurred_on=date(2026, 2, 1),
            description="freelance",
        )
    )
    return repositories


def _open_page(repositories: Repositories) -> AppTest:
    app = AppTest.from_file(str(DASHBOARD_PAGE))
    app.session_state["repositories"] = repositories
    return app.run()


def _select_period(app: AppTest, year: int, month: int) -> None:
    app.number_input[0].set_value(year)
    app.number_input[1].set_value(month)
    app.run()


@pytest.mark.integration
def test_dashboard_page_shows_monthly_summary(tmp_path: Path) -> None:
    app = _open_page(_repositories_with_transactions(tmp_path))

    _select_period(app, 2026, 1)

    assert not app.exception
    assert app.title[0].value == "📊 Resumo mensal"
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["📈 Receitas"] == "R$ 1.500,00"
    assert metrics["📉 Despesas"] == "R$ 500,25"
    assert metrics["💰 Saldo"] == "R$ 999,75"
    assert not any("Nenhuma movimentação" in item.value for item in app.info)


@pytest.mark.integration
def test_dashboard_page_shows_zero_totals_for_empty_month(tmp_path: Path) -> None:
    app = _open_page(_repositories_with_transactions(tmp_path))

    _select_period(app, 2026, 3)

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["📈 Receitas"] == "R$ 0,00"
    assert metrics["📉 Despesas"] == "R$ 0,00"
    assert metrics["💰 Saldo"] == "R$ 0,00"
    assert any("Nenhuma movimentação" in item.value for item in app.info)


@pytest.mark.integration
def test_dashboard_page_shows_negative_balance(tmp_path: Path) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("100.00"),
            occurred_on=date(2026, 1, 5),
            description="receita",
        )
    )
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.EXPENSE,
            amount=Decimal("250.00"),
            occurred_on=date(2026, 1, 6),
            description="despesa",
        )
    )
    app = _open_page(repositories)

    _select_period(app, 2026, 1)

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["💰 Saldo"] == "R$ -150,00"
