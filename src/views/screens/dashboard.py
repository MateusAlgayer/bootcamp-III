"""View do resumo financeiro mensal (RF-005)."""

from datetime import date

import streamlit as st

from controllers.dashboard_controller import DashboardController
from services.balance_service import BalanceService
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import DomainError
from views.formatting import format_currency
from views.repositories import get_repositories

PAGE_TITLE = "📊 Resumo mensal"
EMPTY_MONTH_MESSAGE = "Nenhuma movimentação no período selecionado."
INCOME_LABEL = "📈 Receitas"
EXPENSE_LABEL = "📉 Despesas"
BALANCE_LABEL = "💰 Saldo"


def _controller() -> DashboardController:
    repository = get_repositories().transactions
    return DashboardController(
        MonthlySummaryService(repository), BalanceService(repository)
    )


def render() -> None:
    """Renderiza receitas, despesas e saldo do mês selecionado."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon="📊", layout="wide")
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

    try:
        summary = controller.monthly_summary(year, month)
    except DomainError as error:
        st.error(str(error))
        return

    col_income, col_expense, col_balance = st.columns(3)
    col_income.metric(INCOME_LABEL, format_currency(summary.income))
    col_expense.metric(EXPENSE_LABEL, format_currency(summary.expenses))
    col_balance.metric(BALANCE_LABEL, format_currency(summary.balance))

    if summary.income == 0 and summary.expenses == 0:
        st.info(EMPTY_MONTH_MESSAGE)


if __name__ == "__main__":
    render()
