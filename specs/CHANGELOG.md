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
- cálculo de saldo consolidado como receitas menos despesas em `balance_service` (RF-004);
- resumo mensal de receitas, despesas e saldo em `monthly_summary_service`, controller do
  dashboard e view `dashboard` (RF-005; RNF-FIN-001).

## 0.1.5
- serviço de transações em `src/services/transaction_service.py` (RF-001, RF-002, RF-003):
  `TransactionService` registra receitas e despesas com valor decimal exato (rejeitando
  `float`), data válida e categoria opcional validada, e categoriza transação existente
  recusando transação ou categoria inexistentes sem alterar valor, tipo ou data.

## 0.1.6
- controllers coordenam serviços e views sem regra de negócio própria (ADR-001); erros de
  domínio chegam à view como `DomainError` (ADR-004):
  - `TransactionController` registra receitas/despesas e categoriza transações
    (RF-001, RF-002, RF-003);
  - `DashboardController` passa a expor o saldo consolidado (RF-004) além do resumo
    mensal (RF-005);
  - `BudgetController.compare_with_expenses` compara o orçamento com as despesas
    registradas no período, obtidas do resumo mensal, em vez de um valor digitado na UI
    (RF-006).
