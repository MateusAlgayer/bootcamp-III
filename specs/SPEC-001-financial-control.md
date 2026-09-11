# SPEC-001 — Controle Financeiro Web

Status: **Draft**
Versão: **0.1.0**

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

## 5. Próximos refinamentos

Os contratos de entidades, repositórios, erros e interface serão refinados antes de cada
implementação. Toda mudança deverá ser registrada em `specs/CHANGELOG.md`.
