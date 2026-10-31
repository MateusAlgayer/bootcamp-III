"""View de transações: registro e categorização (RF-001, RF-002, RF-003)."""

from datetime import date

import streamlit as st

from controllers.transaction_controller import TransactionController
from models.category import Category
from models.transaction import Transaction, TransactionType
from services.transaction_service import TransactionService
from shared.errors import DomainError
from views.formatting import format_currency
from views.repositories import get_repositories

PAGE_TITLE = "🧾 Transações"
INCOME_LABEL = "📈 Receita"
EXPENSE_LABEL = "📉 Despesa"
NO_CATEGORY_LABEL = "Sem categoria"
EMPTY_TRANSACTIONS_MESSAGE = "Nenhuma transação registrada ainda."


def _controller() -> TransactionController:
    repositories = get_repositories()
    return TransactionController(
        TransactionService(repositories.transactions, repositories.categories)
    )


def _category_name(categories: tuple[Category, ...], category_id: int | None) -> str:
    for category in categories:
        if category.id == category_id:
            return category.name
    return NO_CATEGORY_LABEL


def _transaction_rows(
    transactions: tuple[Transaction, ...], categories: tuple[Category, ...]
) -> list[dict[str, str | int]]:
    return [
        {
            "ID": transaction.id or 0,
            "Data": transaction.occurred_on.strftime("%d/%m/%Y"),
            "Tipo": (
                INCOME_LABEL
                if transaction.kind is TransactionType.INCOME
                else EXPENSE_LABEL
            ),
            "Descrição": transaction.description,
            "Categoria": _category_name(categories, transaction.category_id),
            "Valor": format_currency(transaction.amount),
        }
        for transaction in transactions
    ]


def _render_registration(controller: TransactionController) -> None:
    categories = controller.list_categories()
    with st.form("transaction_form", clear_on_submit=True):
        col_kind, col_amount = st.columns(2)
        kind = col_kind.radio("Tipo", (INCOME_LABEL, EXPENSE_LABEL), horizontal=True)
        amount_text = col_amount.text_input("Valor (ex.: 1.234,56)")
        col_date, col_description = st.columns(2)
        occurred_on = col_date.date_input("Data", value=date.today())
        description = col_description.text_input("Descrição")
        category = st.selectbox(
            "Categoria (opcional)",
            (None, *categories),
            format_func=lambda item: NO_CATEGORY_LABEL if item is None else item.name,
        )
        submitted = st.form_submit_button("✅ Registrar transação")

    if not submitted:
        return

    category_id = None if category is None else category.id
    try:
        if kind == INCOME_LABEL:
            stored = controller.register_income(
                amount_text, occurred_on, description, category_id
            )
            label = "Receita"
        else:
            stored = controller.register_expense(
                amount_text, occurred_on, description, category_id
            )
            label = "Despesa"
    except DomainError as error:
        st.error(str(error))
        return

    st.success(
        f"{label} registrada: {format_currency(stored.amount)} — "
        f"{stored.description}."
    )


def _render_categorization(controller: TransactionController) -> None:
    transactions = controller.list_transactions()
    uncategorized = [
        transaction for transaction in transactions if transaction.category_id is None
    ]
    categories = controller.list_categories()

    if not transactions:
        st.caption("Nenhuma transação para categorizar.")
        return
    if not uncategorized:
        st.caption("Todas as transações já possuem categoria.")
        return
    if not categories:
        st.info("Nenhuma categoria disponível para categorização.")
        return

    options: dict[str, int] = {}
    for transaction in uncategorized:
        if transaction.id is None:
            continue
        label = (
            f"#{transaction.id} — {transaction.occurred_on:%d/%m/%Y} — "
            f"{transaction.description}"
        )
        options[label] = transaction.id
    selected = st.selectbox("Transação sem categoria", tuple(options))
    category = st.selectbox("Categoria", categories, format_func=lambda item: item.name)
    if st.button("🏷️ Categorizar", key="categorize_transaction"):
        try:
            updated = controller.categorize(options[selected], category.id)
        except DomainError as error:
            st.error(str(error))
        else:
            st.success(f"Transação #{updated.id} categorizada como {category.name}.")


def render() -> None:
    """Renderiza o registro, a categorização e a lista de transações."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🧾", layout="wide")
    st.title(PAGE_TITLE)
    try:
        controller = _controller()
    except DomainError as error:
        st.error(str(error))
        return

    st.subheader("➕ Nova transação")
    _render_registration(controller)

    st.divider()
    st.subheader("🏷️ Categorizar transação")
    _render_categorization(controller)

    st.divider()
    st.subheader("📋 Movimentações registradas")
    transactions = controller.list_transactions()
    if not transactions:
        st.info(EMPTY_TRANSACTIONS_MESSAGE)
        return
    st.dataframe(
        _transaction_rows(transactions, controller.list_categories()),
        hide_index=True,
    )


if __name__ == "__main__":
    render()
