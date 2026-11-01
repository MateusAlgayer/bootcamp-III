import pytest

from views import home as entrypoint
from views.screens import home


@pytest.mark.unit
def test_app_title():
    assert home.APP_TITLE == "ResetMoney"


@pytest.mark.unit
def test_welcome_message():
    assert home.WELCOME_MESSAGE == "Bem-vindo ao ResetMoney!"


@pytest.mark.unit
def test_home_features_have_icon_and_page():
    assert all(icon and page for icon, _, _, page in home.FEATURES)
    assert [page for _, _, _, page in home.FEATURES] == [
        "screens/dashboard.py",
        "screens/budget.py",
        "screens/transactions.py",
    ]


@pytest.mark.unit
def test_sidebar_uses_friendly_titles_and_icons():
    titles = [title for _, title, _ in entrypoint.NAV_ITEMS]
    icons = [icon for _, _, icon in entrypoint.NAV_ITEMS]
    assert titles == ["Início", "Resumo mensal", "Orçamento mensal", "Transações"]
    assert all(icons)
