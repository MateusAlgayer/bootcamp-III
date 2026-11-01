"""Home da aplicação de controle financeiro."""

import streamlit as st

APP_TITLE = "ResetMoney"
APP_ICON = "💰"
WELCOME_MESSAGE = "Bem-vindo ao ResetMoney!"
APP_DESCRIPTION = (
    "Controle suas finanças pessoais em um só lugar: registre movimentações, "
    "acompanhe o saldo e planeje o orçamento de cada mês."
)
PAGE_TITLE = f"{APP_TITLE} — Controle financeiro pessoal"

FEATURES: tuple[tuple[str, str, str, str], ...] = (
    (
        "📊",
        "Resumo mensal",
        "Consulte receitas, despesas e saldo do mês que você escolher.",
        "screens/dashboard.py",
    ),
    (
        "🎯",
        "Orçamento mensal",
        "Defina um limite de despesas e veja quanto já foi consumido.",
        "screens/budget.py",
    ),
    (
        "🧾",
        "Transações",
        "Registre e categorize suas movimentações financeiras.",
        "screens/transactions.py",
    ),
)

STEPS: tuple[tuple[str, str], ...] = (
    ("1️⃣", "Defina o orçamento do mês em **Orçamento mensal**."),
    ("2️⃣", "Registre receitas e despesas em **Transações**."),
    ("3️⃣", "Acompanhe o resultado em **Resumo mensal**."),
)


def render() -> None:
    """Renderiza a página inicial com atalhos para as áreas do app."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon=APP_ICON, layout="wide")

    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(APP_DESCRIPTION)
    st.write(WELCOME_MESSAGE)
    st.divider()

    st.subheader("🚀 O que você pode fazer")
    for column, (icon, name, description, page) in zip(
        st.columns(len(FEATURES)), FEATURES
    ):
        with column, st.container(border=True):
            st.markdown(f"#### {icon} {name}")
            st.write(description)
            st.page_link(page, label=f"Abrir {name.lower()}")

    st.divider()
    st.subheader("🧭 Como começar")
    for icon, step in STEPS:
        st.markdown(f"{icon} {step}")


if __name__ == "__main__":
    render()
