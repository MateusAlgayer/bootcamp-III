import pytest

from views import home


@pytest.mark.unit
def test_app_title():
    assert home.APP_TITLE == "Hello World"


@pytest.mark.unit
def test_welcome_message():
    assert home.WELCOME_MESSAGE == "Bem-vindo ao bootcamp-III!"
