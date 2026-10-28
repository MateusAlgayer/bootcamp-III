from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT_DIR = Path(__file__).resolve().parents[2]
BUDGET_PAGE = ROOT_DIR / "src" / "views" / "pages" / "budget.py"


@pytest.mark.integration
def test_budget_page_defines_and_compares_budget():
    app = AppTest.from_file(str(BUDGET_PAGE)).run()

    assert not app.exception
    assert app.title[0].value == "Orçamento mensal"

    app.text_input[0].input("1500.00")
    app.button[0].click().run()

    assert not app.exception
    assert any("Orçamento de R$ 1500.00" in item.value for item in app.success)

    app.text_input[1].input("350.50")
    app.button[1].click().run()

    assert not app.exception
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Despesas do período"] == "R$ 350.50"
    assert metrics["Saldo do orçamento"] == "R$ 1149.50"
    assert any("23.37% do orçamento" in item.value for item in app.success)


@pytest.mark.integration
def test_budget_page_rejects_non_positive_limit():
    app = AppTest.from_file(str(BUDGET_PAGE)).run()

    app.text_input[0].input("0")
    app.button[0].click().run()

    assert not app.exception
    assert any("maior que zero" in item.value for item in app.error)


@pytest.mark.integration
def test_budget_page_reports_exceeded_budget():
    app = AppTest.from_file(str(BUDGET_PAGE)).run()

    app.text_input[0].input("1000.00")
    app.button[0].click().run()
    app.text_input[1].input("1200.00")
    app.button[1].click().run()

    assert not app.exception
    assert any("Orçamento excedido em R$ 200.00" in item.value for item in app.error)


@pytest.mark.integration
def test_budget_page_requires_budget_before_comparison():
    app = AppTest.from_file(str(BUDGET_PAGE)).run()

    app.text_input[1].input("10.00")
    app.button[1].click().run()

    assert not app.exception
    assert any("não há orçamento vigente" in item.value for item in app.error)
