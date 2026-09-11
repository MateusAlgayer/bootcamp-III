# ADR-002 — Representação monetária exata

- **Status:** Proposed
- **Contexto:** ponto flutuante binário pode introduzir erro de representação em valores monetários.
- **Decisão:** usar `decimal.Decimal` ou centavos inteiros no domínio; proibir `float` em cálculos financeiros.
- **Consequências:** conversões de entrada/saída devem ser explícitas e cobertas por testes.
