"""View do orçamento mensal (RF-006)."""

from datetime import date

import streamlit as st

from controllers.budget_controller import BudgetController
from models.budget import BudgetComparison
from services.budget_service import BudgetService
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import DomainError
from views.formatting import format_currency, format_percentage
from views.repositories import get_repositories

PAGE_TITLE = "🎯 Orçamento mensal"
LIMIT_LABEL = "💰 Limite mensal (ex.: 1500.00)"
SPENT_LABEL = "💸 Despesas do período"
REMAINING_LABEL = "🏦 Saldo do orçamento"
CURRENT_BUDGET_LABEL = "🎯 Orçamento vigente"


def _controller() -> BudgetController:
    repositories = get_repositories()
    return BudgetController(
        BudgetService(repositories.budgets),
        MonthlySummaryService(repositories.transactions),
    )


def _render_comparison(comparison: BudgetComparison) -> None:
    col_spent, col_remaining = st.columns(2)
    col_spent.metric(SPENT_LABEL, format_currency(comparison.spent))
    col_remaining.metric(REMAINING_LABEL, format_currency(comparison.remaining))
    if comparison.exceeded:
        st.error(f"Orçamento excedido em {format_currency(abs(comparison.remaining))}.")
    else:
        st.success(
            f"{format_percentage(comparison.usage_ratio)} do orçamento consumido."
        )


def render() -> None:
    """Renderiza a definição do orçamento e a comparação com despesas."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon="🎯", layout="wide")
    st.title(PAGE_TITLE)
    try:
        controller = _controller()
    except DomainError as error:
        st.error(str(error))
        return
    today = date.today()

    col_year, col_month = st.columns(2)
    year_input = col_year.number_input(
        "🗓️ Ano", min_value=1, max_value=9999, value=today.year, step=1
    )
    month_input = col_month.number_input(
        "📅 Mês", min_value=1, max_value=12, value=today.month, step=1
    )
    year = int(year_input)
    month = int(month_input)

    with st.form("budget_definition"):
        limit_text = st.text_input(LIMIT_LABEL, value="", key="budget_limit")
        submitted = st.form_submit_button("✅ Definir orçamento")

    if submitted:
        try:
            budget = controller.define_budget(year, month, limit_text)
        except DomainError as error:
            st.error(str(error))
        else:
            st.success(
                f"Orçamento de {format_currency(budget.limit)} "
                f"definido para {budget.period.label()}."
            )

    current_budget = controller.find_budget(year, month)
    if current_budget is None:
        st.info("Nenhum orçamento vigente para o período selecionado.")
    else:
        st.metric(CURRENT_BUDGET_LABEL, format_currency(current_budget.limit))

    if st.button("🔍 Comparar com despesas", key="budget_compare"):
        try:
            comparison = controller.compare_with_expenses(year, month)
        except DomainError as error:
            st.error(str(error))
        else:
            _render_comparison(comparison)


if __name__ == "__main__":
    render()
