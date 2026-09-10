import streamlit as st

APP_TITLE = "Hello World"
WELCOME_MESSAGE = "Bem-vindo ao bootcamp-III!"


def render() -> None:
    st.title(APP_TITLE)
    st.write(WELCOME_MESSAGE)


if __name__ == "__main__":
    render()
