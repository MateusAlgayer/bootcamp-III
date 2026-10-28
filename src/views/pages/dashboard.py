"""View do resumo financeiro mensal (RF-005)."""

from datetime import date
from decimal import Decimal

import streamlit as st

from controllers.dashboard_controller import DashboardController
from repositories.memory import InMemoryTransactionRepository
from services.balance_service import BalanceService
from services.monthly_summary_service import MonthlySummaryService
from shared.errors import DomainError

PAGE_TITLE = "Resumo mensal"
EMPTY_MONTH_MESSAGE = "Nenhuma movimentação no período selecionado."


def _controller() -> DashboardController:
    if "transaction_repository" not in st.session_state:
        st.session_state["transaction_repository"] = InMemoryTransactionRepository()
    repository: InMemoryTransactionRepository = st.session_state[
        "transaction_repository"
    ]
    return DashboardController(
        MonthlySummaryService(repository), BalanceService(repository)
    )


def _format_money(value: Decimal) -> str:
    return f"R$ {value:.2f}"


def render() -> None:
    """Renderiza receitas, despesas e saldo do mês selecionado."""
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

    try:
        summary = controller.monthly_summary(year, month)
    except DomainError as error:
        st.error(str(error))
        return

    st.metric("Receitas", _format_money(summary.income))
    st.metric("Despesas", _format_money(summary.expenses))
    st.metric("Saldo", _format_money(summary.balance))

    if summary.income == 0 and summary.expenses == 0:
        st.info(EMPTY_MONTH_MESSAGE)


if __name__ == "__main__":
    render()
