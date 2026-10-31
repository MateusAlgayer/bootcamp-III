# SPEC-001 — Controle Financeiro Web

Status: **Implementado (Entrega 1)**
Versão: **0.1.13**

## 1. Objetivo

Aplicação web para registrar e categorizar movimentações financeiras, calcular saldo,
consolidar um resumo mensal e controlar um limite/orçamento mensal.

A especificação é a fonte de verdade para implementação e testes. Agentes de IA atuam
como camada de revisão e não possuem autoridade para criar requisitos ou alterar contratos.

## 2. Escopo funcional inicial

### RF-001 — Registrar receita
O sistema deve permitir o registro de uma receita com valor monetário positivo, data,
descrição e categoria opcional.

**Critérios de aceite iniciais**
- valor deve ser estritamente maior que zero;
- valor monetário não pode usar `float` no domínio;
- a transação deve ser identificada como `INCOME`;
- data deve ser válida;
- registro criado deve poder ser recuperado pelo repositório.

### RF-002 — Registrar despesa
O sistema deve permitir o registro de uma despesa com valor monetário positivo, data,
descrição e categoria opcional.

**Critérios de aceite iniciais**
- valor deve ser estritamente maior que zero;
- valor monetário não pode usar `float` no domínio;
- a transação deve ser identificada como `EXPENSE`;
- data deve ser válida;
- registro criado deve poder ser recuperado pelo repositório.

### RF-003 — Categorizar transação
O sistema deve permitir associar uma categoria válida a uma transação existente.

**Critérios de aceite iniciais**
- transação inexistente deve ser rejeitada;
- categoria inexistente deve ser rejeitada;
- a categorização não pode alterar valor, tipo ou data da transação.

### RF-004 — Calcular saldo consolidado
O sistema deve calcular o saldo como receitas menos despesas.


`saldo = soma(receitas) - soma(despesas)`

**Critérios de aceite iniciais**
- ausência de transações resulta em saldo zero;
- cálculo deve preservar precisão monetária decimal;
- todas as transações elegíveis no escopo devem ser consideradas exatamente uma vez.

### RF-005 — Exibir resumo financeiro mensal
O sistema deve apresentar um resumo de receitas, despesas e saldo para um mês/ano
selecionado.

**Critérios de aceite iniciais**
- apenas transações pertencentes ao período selecionado podem compor o resumo;
- mês sem movimentações deve produzir totais iguais a zero;
- o saldo mensal deve ser consistente com RF-004 aplicado ao período.

### RF-006 — Definir limite/orçamento mensal
O sistema deve permitir definir um orçamento de despesas para determinado mês/ano.

**Critérios de aceite iniciais**
- orçamento deve ser estritamente maior que zero;
- deve existir no máximo um orçamento vigente por período no escopo inicial;
- o sistema deve permitir comparar despesas do período com o orçamento definido.

## 3. Requisitos não funcionais iniciais

### RNF-FIN-001 — Precisão monetária
Valores monetários do domínio devem utilizar representação decimal exata (`Decimal`)
ou centavos inteiros. `float` é proibido para regras e cálculos financeiros.

### RNF-TEST-001 — Testabilidade
Regras de negócio devem ser testáveis sem inicializar a interface Streamlit.

### RNF-SDD-001 — Rastreabilidade
Mudanças funcionais devem referenciar pelo menos um requisito RF/RNF e possuir casos de
teste correspondentes.

### RNF-AI-001 — Autoridade do agente
Agentes de IA podem revisar especificação, diff e testes, mas não podem inventar requisitos,
modificar a especificação silenciosamente nem aprovar merge em substituição ao revisor humano.

## 4. Fora de escopo da Entrega 1

- integração bancária/Open Finance;
- pagamentos reais;
- autenticação financeira de produção;
- recomendação de investimento;
- machine learning;
- agentes alterando código de produção de forma autônoma.

## 5. Estado de implementação (Entrega 1)

Os critérios de aceite das seções 2 e 3 não foram alterados. O estado abaixo reflete a
implementação verificada pelos gates locais.

| Requisito | Estado | Evidência principal |
|---|---|---|
| RF-001 | Implementado | `transaction_service`, `transaction_controller`, view `transactions` e persistência SQLite; testes unitários, de contrato e de integração |
| RF-002 | Implementado | mesmo fluxo do RF-001 para despesas |
| RF-003 | Implementado | categorização no service/controller, na view `transactions` e persistência SQLite; testes unitários e de integração |
| RF-004 | Implementado no domínio/controller | `balance_service` e `DashboardController.consolidated_balance`; sem tela dedicada |
| RF-005 | Implementado | `monthly_summary_service`, `DashboardController` e view `dashboard` |
| RF-006 | Implementado | `budget_service`, `BudgetController`, view `budget` e persistência SQLite |
| RNF-FIN-001 | Implementado | `shared.money` com `Decimal`/`Money`; centavos inteiros no SQLite; `float` rejeitado |
| RNF-TEST-001 | Implementado | testes unitários sem Streamlit; UI exercitada com `streamlit.testing.v1.AppTest` |
| RNF-SDD-001 | Implementado | `specs/TRACEABILITY.md` e `specs/CHANGELOG.md` |
| RNF-AI-001 | Em processo | `AGENTS.md` e ADR-003; revisão e merge permanecem humanos |

### 5.1 Pendências conhecidas

- **Persistência:** a aplicação usa SQLite local em `DATABASE_PATH` (padrão
  `data/finance.db`), criado automaticamente a partir de `repositories/sqlite_schema.sql`.
  O Docker Compose persiste o arquivo no volume `finance-data`. O adaptador em memória
  permanece restrito a testes.
- **Categorias:** as categorias iniciais são semeadas automaticamente; não há CRUD de
  categorias previsto nesta SPEC.
- **RF-004 na UI:** o saldo consolidado é calculado, mas nenhuma tela o apresenta; a UI
  mostra o saldo mensal do RF-005.
- **Migrações:** o esquema é criado com `CREATE TABLE IF NOT EXISTS`; evoluções futuras
  exigem migração manual/versionada.
- **ADRs:** ADR-001 a ADR-005 e ADR-007 estão aceitas; a ADR-006 (Supabase) foi substituída
  pela ADR-007 (SQLite local).

## 6. Próximos refinamentos

Mudanças de requisito continuam exigindo atualização explícita desta SPEC e registro em
`specs/CHANGELOG.md`.
