# ADR-005 — Gates de qualidade e segurança como política de CI

- **Status:** Proposed
- **Contexto:** `pyproject.toml` e `.github/workflows/ci.yml` já aplicam lint/formatação, `mypy
  --strict`, SAST (`bandit`), SCA (`pip-audit`), SBOM e cobertura mínima de testes, mas o racional
  dessa política não estava registrado.
- **Decisão:** manter os quatro grupos de verificação (quality, security, tests, coverage) em
  `push` (informativo) e `pull_request` (gate de merge) para `main`/`dev`, com `mypy --strict` e
  cobertura mínima de 85%.
- **Consequências:** feedback antecipado ao desenvolvedor e segurança validada desde o primeiro
  push; pipeline mais longo, com duplicação de steps entre `push` e `pull_request`.
