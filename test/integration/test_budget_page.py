from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from models.transaction import Transaction, TransactionType
from repositories.memory import InMemoryTransactionRepository

ROOT_DIR = Path(__file__).resolve().parents[2]
BUDGET_PAGE = ROOT_DIR / "src" / "views" / "pages" / "budget.py"


def _repository_with_expenses(*amounts: str) -> InMemoryTransactionRepository:
    repository = InMemoryTransactionRepository()
    for amount in amounts:
        repository.add(
            Transaction(
                kind=TransactionType.EXPENSE,
                amount=Decimal(amount),
                occurred_on=date(2026, 1, 15),
                description="despesa",
            )
        )
    return repository


def _open_page(repository: InMemoryTransactionRepository) -> AppTest:
    app = AppTest.from_file(str(BUDGET_PAGE)).run()
    app.session_state["transaction_repository"] = repository
    app.number_input[0].set_value(2026)
    app.number_input[1].set_value(1)
    return app.run()


@pytest.mark.integration
def test_budget_page_defines_and_compares_budget():
    app = _open_page(_repository_with_expenses("300.00", "50.50"))

    assert not app.exception
    assert app.title[0].value == "Orçamento mensal"

    app.text_input[0].input("1500.00")
    app.button[0].click().run()

    assert not app.exception
    assert any("Orçamento de R$ 1500.00" in item.value for item in app.success)

    app.button[1].click().run()

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Despesas do período"] == "R$ 350.50"
    assert metrics["Saldo do orçamento"] == "R$ 1149.50"
    assert any("23.37% do orçamento" in item.value for item in app.success)


@pytest.mark.integration
def test_budget_page_rejects_non_positive_limit():
    app = _open_page(InMemoryTransactionRepository())

    app.text_input[0].input("0")
    app.button[0].click().run()

    assert not app.exception
    assert any("maior que zero" in item.value for item in app.error)


@pytest.mark.integration
def test_budget_page_reports_exceeded_budget():
    app = _open_page(_repository_with_expenses("1200.00"))

    app.text_input[0].input("1000.00")
    app.button[0].click().run()
    app.button[1].click().run()

    assert not app.exception
    assert any("Orçamento excedido em R$ 200.00" in item.value for item in app.error)


@pytest.mark.integration
def test_budget_page_requires_budget_before_comparison():
    app = _open_page(_repository_with_expenses("10.00"))

    app.button[1].click().run()

    assert not app.exception
    assert any("não há orçamento vigente" in item.value for item in app.error)
