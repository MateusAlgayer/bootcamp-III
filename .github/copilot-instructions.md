# Instruções para o GitHub Copilot

A fonte única das regras é `AGENTS.md`. Leia antes de sugerir código. Este resumo é
**não normativo**: em caso de divergência, vale `AGENTS.md`.

## Invariantes

- Dinheiro usa `Decimal` ou centavos inteiros; `float` é proibido no domínio (RNF-FIN-001).
- `mypy --strict`, `black` com 88 colunas e `isort` profile `black`; Python 3.12, layout `src/`.
- Camadas: `views -> controllers -> services -> repositories`, com `models`/`shared` como
  folhas; `services` não importam Streamlit.
- Toda mudança de comportamento exige teste `pytest`; cobertura mínima de 85% com branch.
- Não invente requisitos: a fonte é `specs/SPEC-001-financial-control.md` e os ADRs em `docs/adr/`.
