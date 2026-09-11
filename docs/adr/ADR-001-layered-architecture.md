# ADR-001 — Arquitetura em camadas sobre a base MVC

- **Status:** Proposed
- **Contexto:** o repositório já possui `models`, `controllers` e `views`. O domínio financeiro
  precisa permanecer testável sem Streamlit e sem acoplamento direto ao armazenamento.
- **Decisão:** preservar MVC e introduzir `services`, `repositories` e `shared`.
- **Consequências:** regras financeiras ficam fora da UI; persistência pode ser substituída
  nos testes; aumenta ligeiramente o número de módulos.
