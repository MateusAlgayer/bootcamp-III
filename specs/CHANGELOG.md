# Changelog da Especificação

## 0.1.0
- baseline inicial dos RF-001 a RF-006;
- inclusão de precisão monetária, testabilidade, rastreabilidade e autoridade dos agentes.

## 0.1.1
- implementação do tipo primitivo monetário `Money` em `src/shared/money.py` (RNF-FIN-001).

## 0.1.2
- hierarquia de erros de domínio em `src/shared/errors.py` (ADR-004);
- entidades `Transaction` e `Category` em `src/models/` (RF-001, RF-002, RF-003).

## 0.1.3
- contratos `TransactionRepository` e `CategoryRepository` com adaptadores em memória e
  Supabase (RF-001, RF-002, RF-003; ADR-004, ADR-006 proposta).
