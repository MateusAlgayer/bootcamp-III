from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryTransactionRepository

ROOT_DIR = Path(__file__).resolve().parents[2]
DASHBOARD_PAGE = ROOT_DIR / "src" / "views" / "pages" / "dashboard.py"


def _repository_with_transactions() -> InMemoryTransactionRepository:
    repository = InMemoryTransactionRepository()
    repository.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("1500.00"),
            occurred_on=date(2026, 1, 5),
            description="salário",
        )
    )
    repository.add(
        Transaction(
            kind=TransactionType.EXPENSE,
            amount=Decimal("500.25"),
            occurred_on=date(2026, 1, 20),
            description="aluguel",
        )
    )
    repository.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("300.00"),
            occurred_on=date(2026, 2, 1),
            description="freelance",
        )
    )
    return repository


def _select_period(app: AppTest, year: int, month: int) -> None:
    app.number_input[0].set_value(year)
    app.number_input[1].set_value(month)
    app.run()


@pytest.mark.integration
def test_dashboard_page_shows_monthly_summary():
    app = AppTest.from_file(str(DASHBOARD_PAGE)).run()
    app.session_state["transaction_repository"] = _repository_with_transactions()

    _select_period(app, 2026, 1)

    assert not app.exception
    assert app.title[0].value == "Resumo mensal"
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Receitas"] == "R$ 1500.00"
    assert metrics["Despesas"] == "R$ 500.25"
    assert metrics["Saldo"] == "R$ 999.75"
    assert not any("Nenhuma movimentação" in item.value for item in app.info)


@pytest.mark.integration
def test_dashboard_page_shows_zero_totals_for_empty_month():
    app = AppTest.from_file(str(DASHBOARD_PAGE)).run()
    app.session_state["transaction_repository"] = _repository_with_transactions()

    _select_period(app, 2026, 3)

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Receitas"] == "R$ 0.00"
    assert metrics["Despesas"] == "R$ 0.00"
    assert metrics["Saldo"] == "R$ 0.00"
    assert any("Nenhuma movimentação" in item.value for item in app.info)


@pytest.mark.integration
def test_dashboard_page_shows_negative_balance():
    repository = InMemoryTransactionRepository()
    repository.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("100.00"),
            occurred_on=date(2026, 1, 5),
            description="receita",
        )
    )
    repository.add(
        Transaction(
            kind=TransactionType.EXPENSE,
            amount=Decimal("250.00"),
            occurred_on=date(2026, 1, 6),
            description="despesa",
        )
    )
    app = AppTest.from_file(str(DASHBOARD_PAGE)).run()
    app.session_state["transaction_repository"] = repository

    _select_period(app, 2026, 1)

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Saldo"] == "R$ -150.00"
