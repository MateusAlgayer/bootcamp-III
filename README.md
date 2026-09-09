# bootcamp-III

Repositório para tarefas relacionadas a disciplina de bootcamp III

## Configuração

### Pré-requisitos

- Python 3.12+

### Criar o ambiente virtual e instalar as dependências

Em qualquer sistema operacional, rode o script de configuração:

```bash
python configure.py
```

Ele cria o venv, instala as dependências (incluindo dev), instala o pre-commit e roda os hooks em todos os arquivos.

Equivalente manual (Linux/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Rodando o projeto

Rode o frontend (Streamlit):

```bash
streamlit run src/views/home.py
```

## Ferramentas de desenvolvimento

Formatar o código:

```bash
black src test
```

Ordenar as importações:

```bash
isort src test
```

Verificar estilo e erros:

```bash
flake8 src test
```

### Pre-commit

Instalar os hooks (rodam black, isort e flake8 a cada commit):

```bash
pre-commit install
```

## Testes

```bash
pytest test/unit
```
