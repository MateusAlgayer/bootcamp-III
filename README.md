# ResetMoney — Controle Financeiro Web

Aplicação web para registrar e categorizar movimentações financeiras, calcular saldo,
consolidar um resumo mensal e controlar um limite/orçamento mensal, desenvolvida como
atividade da disciplina de bootcamp III.

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

Ou via Docker:

```bash
docker build -t bootcamp-iii .
docker run -p 80:80 bootcamp-iii
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

## Estrutura arquitetural inicial

A aplicação evolui sobre a base MVC existente e separa regras financeiras da interface:

```text
src/
├── models/        # entidades do domínio financeiro
├── services/      # casos de uso e regras de negócio
├── repositories/  # contratos e adaptadores de persistência
├── controllers/   # coordenação entre UI e aplicação
├── views/         # interface Streamlit
└── shared/        # tipos/erros compartilhados, incluindo dinheiro

specs/            # fonte de verdade do fluxo SDD
docs/adr/          # decisões arquiteturais
test/
├── unit/
├── integration/
├── contract/
└── fixtures/
```

A especificação funcional inicial está em `specs/SPEC-001-financial-control.md` e contém
os requisitos RF-001 a RF-006. Agentes de IA atuam como camada de revisão; regras de
autoridade e contexto estão em `AGENTS.md`.

## ADRs

Decisões arquiteturais relevantes ficam registradas em `docs/adr/`:

- [ADR-001 — Arquitetura em camadas sobre a base MVC](docs/adr/ADR-001-layered-architecture.md)
- [ADR-002 — Representação monetária exata](docs/adr/ADR-002-money-representation.md)
- [ADR-003 — Agentes de IA como camada de revisão](docs/adr/ADR-003-ai-review-layer.md)
- [ADR-004 — Hierarquia de exceções de domínio/aplicação](docs/adr/ADR-004-domain-error-handling.md)
- [ADR-005 — Gates de qualidade e segurança como política de CI](docs/adr/ADR-005-ci-quality-security-gates.md)
