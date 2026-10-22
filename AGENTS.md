# Regras para agentes

## Fonte de verdade
- `specs/SPEC-001-financial-control.md`
- `specs/TRACEABILITY.md`
- ADRs aprovados em `docs/adr/`

## Autoridade
1. Não inventar requisitos.
2. Não modificar contratos funcionais sem apontar o RF/RNF afetado.
3. Não tratar saída do agente como substituta de testes determinísticos.
4. Toda mudança comportamental deve possuir teste correspondente.
5. Valores monetários do domínio não podem usar `float`.
6. Revisões devem separar erro confirmado, risco e sugestão.
7. Merge permanece decisão humana após os gates de CI.

## Fluxo de trabalho
1. Antes de codar, leia a SPEC, a TRACEABILITY e os ADRs aplicáveis e identifique o RF/RNF.
2. Faça a menor mudança que satisfaz o requisito; não misture refatoração fora de escopo.
3. Escreva ou atualize o teste determinístico junto com a mudança.
4. Atualize `specs/TRACEABILITY.md` (estado do requisito) e `specs/CHANGELOG.md` quando a
   mudança for funcional.
5. Rode os gates locais da seção "Definição de pronto" antes de abrir PR.

## Estilo e ferramentas
A configuração vive em `pyproject.toml`, `.flake8` e `.pre-commit-config.yaml`. Não crie
configuração paralela nem exceções locais.

- Python 3.12+, layout `src/`.
- Formatação: `black` (88 colunas) e `isort` (profile `black`).
- Lint: `flake8` (máx. 88; `E203`/`W503` ignorados).
- Tipos: `mypy --strict` em `src`. Toda função relevante tem anotação completa; evite `Any`
  desnecessário; `# type: ignore[...]` só com código de erro específico e justificativa.
- Nomes: `snake_case` para módulos, funções e variáveis; `PascalCase` para classes;
  `UPPER_SNAKE_CASE` para constantes de módulo; prefixo `_` para uso interno.
  Identificadores em inglês; documentação, mensagens de erro e comentários em português.
- Docstrings em módulos e APIs públicas, no estilo já existente (`"""Resumo em uma linha."""`).
- Comentários explicam *por que*, não *o que*. Sem código comentado e sem `TODO` sem dono.
- Sem `print` em `src/` (a UI fala via Streamlit; o domínio não fala com a UI).
- Sem estado global mutável; dependências são injetadas por parâmetro/construtor.
- Prefira funções curtas e coesas; se um bloco precisa de comentário para se explicar,
  considere extrair uma função com nome descritivo.

## Arquitetura
- Dependências apontam para dentro: `views -> controllers -> services -> repositories`,
  com `models` e `shared` como folhas. Import no sentido inverso é erro de arquitetura.
- `services`, `models`, `repositories` e `shared` não importam `streamlit` (RNF-TEST-001).
- `views` só apresenta dados e chama controllers; nenhuma regra financeira na view.
- Contratos de persistência ficam em `repositories/contracts.py`; a implementação concreta em
  `repositories/sqlite.py`. SQL não sai da camada `repositories`.
- Erros técnicos são reencapsulados antes de cruzar a fronteira do repositório (ADR-004).
- Não introduza camada, padrão ou abstração nova sem ADR correspondente.

## Dinheiro
- Use `Decimal` ou centavos inteiros em todo o domínio (RNF-FIN-001, ADR-002).
- `float` é proibido em `models`, `services`, `shared` e em qualquer cálculo financeiro.
- Converta na borda (UI/armazenamento) e cubra a conversão com teste: `Decimal(str(valor))`,
  nunca `Decimal(float)`.
- Ao persistir ou exibir, use `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` explícito.
- Compare valores monetários como `Decimal`; não misture `Decimal` e `float` em expressões.

## Erros
- Toda exceção de domínio herda da raiz em `shared/errors.py`, com subtipos para validação,
  não encontrado e conflito.
- Proibido `except:` e `except Exception: pass`. Capture o tipo esperado, reencapsule ou propague.
- A mensagem descreve a regra violada e, quando aplicável, o RF correspondente.

## Testes
- `pytest`, com testes em `test/unit`, `test/integration` e `test/contract`, marcados com
  `@pytest.mark.unit`, `@pytest.mark.integration` ou `@pytest.mark.contract`.
- Nomeie como `test_<comportamento>_<condição>`; um comportamento por teste.
- Determinismo: sem rede, sem `sleep`, sem depender de ordem de execução ou do relógio real;
  use fixtures e `tmp_path`.
- Cada RF alterado precisa de caso de sucesso e de borda/falha; casos de dinheiro afirmam o
  `Decimal` exato.
- Cobertura mínima de 85% com branch (`--cov-fail-under=85`). Não baixe o limite nem use
  `# pragma: no cover` para esconder lógica.
- Testes de unidade não inicializam Streamlit; a UI é exercitada com
  `streamlit.testing.v1.AppTest` em `test/integration`.

## Segurança
- Nunca commite segredos, chaves, `.env` ou artefatos gerados; `gitleaks` roda no pre-commit.
- Sem `eval`/`exec`, sem `pickle` de dados não confiáveis e sem `shell=True` com entrada externa.
- SQL sempre parametrizado; nunca interpole valores em query por formatação de string.
- `bandit` e `pip-audit` devem passar; dependência nova precisa de justificativa no PR.

## Git e PR
- Commits convencionais: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`, `ci:`.
- Branches: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `test/<slug>`, `chore/<slug>`.
- O PR informa: RF/RNF afetado, comportamento alterado, testes executados e riscos.
- Não commite direto em `main`/`dev`; o merge é decisão humana (RNF-AI-001).

## Regras específicas para o agente de IA
- Não altere SPEC ou ADR para acomodar o código; aponte a divergência.
- Não ajuste teste para fazer o código passar quando o requisito não foi atendido.
- Não rode comandos destrutivos (`reset --hard`, `push --force`, remoção de arquivos não
  gerados) sem pedido explícito.
- Em revisões, separe sempre: erro confirmado, risco e sugestão.
- Relate os comandos executados e o resultado real; não declare gate verde sem tê-lo rodado.

## Definição de pronto

```bash
black --check src test
isort --check-only src test
flake8 src test
mypy src --strict
bandit -c pyproject.toml -r src
pytest test --cov=src --cov-branch --cov-fail-under=85
```

- [ ] Todos os comandos acima passam.
- [ ] `specs/TRACEABILITY.md` reflete o estado real do requisito.
- [ ] Nenhuma mudança de comportamento sem teste correspondente.
