from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT_DIR = Path(__file__).resolve().parents[2]


@pytest.mark.integration
def test_home_page_renders():
    app = AppTest.from_file(ROOT_DIR / "src" / "views" / "home.py").run()

    assert not app.exception
    assert app.title[0].value == "Hello World"
    assert "Bem-vindo ao bootcamp-III!" in app.markdown[0].value
