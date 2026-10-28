"""View do orçamento mensal (RF-006)."""

from datetime import date

import streamlit as st

from controllers.budget_controller import BudgetController
from models.budget import BudgetComparison
from repositories.memory import (
    InMemoryBudgetRepository,
    InMemoryTransactionRepository,
)
from services.budget_service import BudgetService
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import DomainError

PAGE_TITLE = "Orçamento mensal"
LIMIT_LABEL = "Limite mensal (ex.: 1500.00)"


def _controller() -> BudgetController:
    if "budget_repository" not in st.session_state:
        st.session_state["budget_repository"] = InMemoryBudgetRepository()
    if "transaction_repository" not in st.session_state:
        st.session_state["transaction_repository"] = InMemoryTransactionRepository()
    budgets: InMemoryBudgetRepository = st.session_state["budget_repository"]
    transactions: InMemoryTransactionRepository = st.session_state[
        "transaction_repository"
    ]
    return BudgetController(BudgetService(budgets), MonthlySummaryService(transactions))


def _render_comparison(comparison: BudgetComparison) -> None:
    st.metric("Despesas do período", f"R$ {comparison.spent:.2f}")
    st.metric("Saldo do orçamento", f"R$ {comparison.remaining:.2f}")
    if comparison.exceeded:
        st.error(f"Orçamento excedido em R$ {abs(comparison.remaining):.2f}.")
    else:
        st.success(f"{comparison.usage_ratio * 100:.2f}% do orçamento consumido.")


def render() -> None:
    """Renderiza a definição do orçamento e a comparação com despesas."""
    st.title(PAGE_TITLE)
    controller = _controller()
    today = date.today()

    col_year, col_month = st.columns(2)
    year_input = col_year.number_input(
        "Ano", min_value=1, max_value=9999, value=today.year, step=1
    )
    month_input = col_month.number_input(
        "Mês", min_value=1, max_value=12, value=today.month, step=1
    )
    year = int(year_input)
    month = int(month_input)

    with st.form("budget_definition"):
        limit_text = st.text_input(LIMIT_LABEL, value="", key="budget_limit")
        submitted = st.form_submit_button("Definir orçamento")

    if submitted:
        try:
            budget = controller.define_budget(year, month, limit_text)
        except DomainError as error:
            st.error(str(error))
        else:
            st.success(
                f"Orçamento de R$ {budget.limit:.2f} "
                f"definido para {budget.period.label()}."
            )

    current_budget = controller.find_budget(year, month)
    if current_budget is None:
        st.info("Nenhum orçamento vigente para o período selecionado.")
    else:
        st.metric("Orçamento vigente", f"R$ {current_budget.limit:.2f}")

    if st.button("Comparar com despesas", key="budget_compare"):
        try:
            comparison = controller.compare_with_expenses(year, month)
        except DomainError as error:
            st.error(str(error))
        else:
            _render_comparison(comparison)


if __name__ == "__main__":
    render()
