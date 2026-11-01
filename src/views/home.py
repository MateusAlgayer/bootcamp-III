"""Ponto de entrada e navegação lateral da aplicação."""

import streamlit as st

NAV_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("screens/home.py", "Início", "🏠"),
    ("screens/dashboard.py", "Resumo mensal", "📊"),
    ("screens/budget.py", "Orçamento mensal", "🎯"),
    ("screens/transactions.py", "Transações", "🧾"),
)


def render() -> None:
    """Define a sidebar com os nomes e ícones das telas."""
    pages = [st.Page(path, title=title, icon=icon) for path, title, icon in NAV_ITEMS]
    st.navigation(pages).run()


if __name__ == "__main__":
    render()
