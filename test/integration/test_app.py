import importlib
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT_DIR = Path(__file__).resolve().parents[2]
PAGE_MODULES = (
    "screens.home",
    "screens.dashboard",
    "screens.budget",
    "screens.transactions",
)


@pytest.mark.integration
def test_pages_import_with_views_directory_first(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reproduz o `sys.path` usado pelo Streamlit ao executar as páginas.

    O bootstrap do Streamlit insere o diretório do script principal
    (`src/views`) no início do `sys.path`. Um módulo dessa pasta com nome de
    pacote de domínio (ex.: `repositories.py`) sombrearia o pacote real.
    """
    monkeypatch.syspath_prepend(str(ROOT_DIR / "src" / "views"))

    for name in PAGE_MODULES:
        module = importlib.import_module(name)

        assert callable(module.render)


@pytest.mark.integration
def test_home_page_renders():
    app = AppTest.from_file(ROOT_DIR / "src" / "views" / "home.py").run()

    assert not app.exception
    assert app.title[0].value == "💰 ResetMoney"
    markdown = "\n".join(item.value for item in app.markdown)
    assert "Bem-vindo ao ResetMoney!" in markdown
    subheaders = [item.value for item in app.subheader]
    assert "🚀 O que você pode fazer" in subheaders
    assert "🧭 Como começar" in subheaders
