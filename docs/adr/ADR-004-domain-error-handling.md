# ADR-004 — Hierarquia de exceções de domínio/aplicação

- **Status:** Proposed
- **Contexto:** `shared/errors.py` está vazio; regras de RF-001, RF-002, RF-003 e RF-006 geram
  falhas que precisam chegar de `services` a `controllers` e à view sem expor exceções técnicas
  de infraestrutura.
- **Decisão:** definir em `shared/errors.py` uma exceção raiz e subtipos (validação, não
  encontrado, conflito); `repositories` reencapsulam erros técnicos antes de propagá-los.
- **Consequências:** a view não lida com exceções de storage; testes podem asserir o tipo de erro
  de domínio esperado; exige disciplina para nunca deixar uma exceção técnica escapar sem
  reencapsulamento.
