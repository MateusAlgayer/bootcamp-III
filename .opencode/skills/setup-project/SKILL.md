---
name: setup-project
description: Use when the user asks to configure, set up, install dependencies, create venv, or bootstrap this project (bootcamp-III). Runs the reproducible setup: Python venv, editable install with dev extras, pre-commit hooks.
---

# Setup do projeto (bootcamp-III)

Use quando o usuário pedir para configurar/inicializar o projeto, criar o ambiente virtual, instalar dependências ou preparar o pre-commit.

## Estrutura do projeto

- `pyproject.toml` — dependências e config de black/isort/flake8 (layout `src/`, Python 3.12+)
- `configure.py` — script cross-platform que executa toda a configuração
- `src/` — MVC preservado e complementado por `services/`, `repositories/` e `shared/`
- `test/unit/` — testes
- `.pre-commit-config.yaml` — hooks black (check), isort (check-only) e flake8
- `Dockerfile` — imagem `python:3.12-alpine` que roda o Streamlit na porta 80

## Como configurar

1. Verifique se Python 3.12+ está disponível (`python --version`).
2. Execute o script de configuração:

   ```bash
   python configure.py
   ```

   Ele cria o `.venv` (se não existir), instala o pacote em modo editável com as extras `[dev]`,
   instala os hooks do pre-commit e roda os hooks em todos os arquivos.

Alternativa manual (Linux/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Em Windows, use `.venv\Scripts\activate` em vez de `source`.

## Verificação

Confirme que a instalação funcionou:

```bash
.venv/bin/python -c "import streamlit; print(streamlit.__version__)"
.venv/bin/pre-commit run --all-files
```

## Rodar o app

```bash
.venv/bin/streamlit run src/views/home.py
```

Ou em container:

```bash
docker build -t bootcamp-iii .
docker run -p 80:80 bootcamp-iii
```
