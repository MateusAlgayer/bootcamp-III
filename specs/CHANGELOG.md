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

## 0.1.7
- UI em português com ícones e nova Home com atalhos para resumo mensal, orçamento e
  transações (RF-005, RF-006; RNF-SDD-001);
- página de transações exibe aviso de funcionalidade pendente de refinamento da SPEC.

## 0.1.8
- valores monetários e percentuais da UI formatados no padrão brasileiro, com
  arredondamento explícito `ROUND_HALF_UP` (ex.: `R$ 1.234,56` e `23,37%`).

## 0.1.9
- navegação lateral definida com `st.navigation`/`st.Page`, com títulos e ícones em
  português (`Início`, `Resumo mensal`, `Orçamento mensal`, `Transações`);
- telas movidas de `views/pages/` para `views/screens/` para evitar o multipage
  automático do Streamlit.

## 0.1.10
- view de transações em `src/views/screens/transactions.py` com registro de receita e
  despesa, categorização e listagem das movimentações (RF-001, RF-002, RF-003);
- consultas `list_transactions` e `list_categories` no service e no controller de
  transações para alimentar a UI;
- categorias iniciais no adaptador em memória para tornar a categorização utilizável na
  interface.

## 0.1.11
- revisão da SPEC-001: status e versão alinhados ao changelog, com seção de estado de
  implementação e pendências conhecidas;
- matriz de rastreabilidade ampliada para RNF-TEST-001, RNF-SDD-001 e RNF-AI-001;
- RF-004 registrado como implementado no domínio/controller, sem tela dedicada.

## 0.1.12
- ADR-001 a ADR-006 aceitas formalmente;
- SQLite removido; Supabase (ADR-006) é a única persistência definida, com adaptador em
  `repositories/supabase_adapter.py` e esquema em `repositories/supabase_schema.sql`;
- `AGENTS.md`, SPEC-001 e matriz de rastreabilidade alinhados à decisão.

## 0.1.13
- persistência migrada para SQLite local em `repositories/sqlite.py`, com valores em
  centavos inteiros e esquema em `repositories/sqlite_schema.sql` (ADR-007);
- execução local padronizada via `docker-compose.yml`, com volume `finance-data` para o
  banco;
- Supabase removido do código, das dependências e dos testes; ADR-006 marcada como
  substituída pela ADR-007;
- categorias iniciais semeadas automaticamente no primeiro acesso.
