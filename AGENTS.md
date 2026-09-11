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
