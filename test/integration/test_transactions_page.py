from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from models.transaction import Transaction, TransactionType
from views.bootstrap import Repositories, build_repositories

ROOT_DIR = Path(__file__).resolve().parents[2]
TRANSACTIONS_PAGE = ROOT_DIR / "src" / "views" / "screens" / "transactions.py"


def _open_page(repositories: Repositories | None = None) -> AppTest:
    app = AppTest.from_file(str(TRANSACTIONS_PAGE))
    if repositories is not None:
        app.session_state["repositories"] = repositories
    return app.run()


def _fill_form(
    app: AppTest,
    *,
    kind: str,
    amount: str,
    occurred_on: date,
    description: str,
    category_index: int = 0,
) -> AppTest:
    app.radio[0].set_value(kind)
    app.text_input[0].input(amount)
    app.date_input[0].set_value(occurred_on)
    app.text_input[1].input(description)
    app.selectbox[0].select_index(category_index)
    return app.button[0].click().run()


@pytest.mark.integration
def test_transactions_page_registers_expense_with_category(tmp_path: Path) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    app = _open_page(repositories)

    _fill_form(
        app,
        kind="📉 Despesa",
        amount="42,50",
        occurred_on=date(2026, 1, 15),
        description="Feira",
        category_index=1,
    )

    assert not app.exception
    assert any("Despesa registrada: R$ 42,50" in item.value for item in app.success)
    stored = repositories.transactions.list_all()
    assert len(stored) == 1
    assert stored[0].kind is TransactionType.EXPENSE
    assert stored[0].amount == Decimal("42.50")
    assert stored[0].category_id == 1


@pytest.mark.integration
def test_transactions_page_registers_income_without_category(
    tmp_path: Path,
) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    app = _open_page(repositories)

    _fill_form(
        app,
        kind="📈 Receita",
        amount="1.500,00",
        occurred_on=date(2026, 1, 5),
        description="Salário",
    )

    assert not app.exception
    assert any("Receita registrada: R$ 1.500,00" in item.value for item in app.success)
    stored = repositories.transactions.list_all()
    assert len(stored) == 1
    assert stored[0].kind is TransactionType.INCOME
    assert stored[0].amount == Decimal("1500.00")
    assert stored[0].category_id is None


@pytest.mark.integration
def test_transactions_page_rejects_non_positive_amount(tmp_path: Path) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    app = _open_page(repositories)

    _fill_form(
        app,
        kind="📉 Despesa",
        amount="0",
        occurred_on=date(2026, 1, 15),
        description="Feira",
    )

    assert not app.exception
    assert any("maior que zero" in item.value for item in app.error)
    assert repositories.transactions.list_all() == ()


@pytest.mark.integration
def test_transactions_page_lists_registered_transactions(tmp_path: Path) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    repositories.transactions.add(
        Transaction(
            kind=TransactionType.INCOME,
            amount=Decimal("100.00"),
            occurred_on=date(2026, 1, 5),
            description="Salário",
        )
    )
    app = _open_page(repositories)

    assert not app.exception
    assert len(app.dataframe) == 1
    table = str(app.dataframe[0].value)
    assert "Salário" in table
    assert "R$ 100,00" in table
    assert "📈 Receita" in table


@pytest.mark.integration
def test_transactions_page_categorizes_uncategorized_transaction(
    tmp_path: Path,
) -> None:
    repositories = build_repositories(tmp_path / "finance.db")
    stored = repositories.transactions.add(
        Transaction(
            kind=TransactionType.EXPENSE,
            amount=Decimal("42.50"),
            occurred_on=date(2026, 1, 15),
            description="Feira",
        )
    )
    app = _open_page(repositories)

    app.selectbox[1].select_index(0)
    app.selectbox[2].select_index(1)
    app.button[1].click().run()

    assert not app.exception
    assert any("categorizada como Lazer" in item.value for item in app.success)
    assert stored.id is not None
    updated = repositories.transactions.get(stored.id)
    assert updated is not None
    assert updated.category_id == 4


@pytest.mark.integration
def test_transactions_page_shows_empty_state() -> None:
    app = _open_page()

    assert not app.exception
    assert any("Nenhuma transação registrada ainda." in item.value for item in app.info)
    assert any(
        "Nenhuma transação para categorizar." in item.value for item in app.caption
    )
