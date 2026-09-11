# ADR-003 — Agentes de IA como camada de revisão

- **Status:** Proposed
- **Contexto:** a Entrega 1 exige uso documentado de agente e validação automatizada.
- **Decisão:** agentes revisarão SPEC, diff e testes após os gates determinísticos. Não terão
  autoridade autônoma para alterar requisitos ou substituir aprovação humana.
- **Consequências:** o resultado do agente é evidência complementar e auditável, não oráculo de aprovação.
