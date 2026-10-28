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

## 0.1.4
- serviço de transações em `src/services/transaction_service.py` (RF-001, RF-002, RF-003):
  `TransactionService` registra receitas e despesas com valor decimal exato (rejeitando
  `float`), data válida e categoria opcional validada, e categoriza transação existente
  recusando transação ou categoria inexistentes sem alterar valor, tipo ou data.
- serviço de saldo consolidado em `src/services/balance_service.py` (RF-004):
  `BalanceService` calcula receitas menos despesas a partir do repositório de transações,
  com precisão decimal exata, saldo zero quando vazio e cada transação contada uma vez.
