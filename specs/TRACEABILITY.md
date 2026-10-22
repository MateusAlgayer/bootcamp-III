# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service` | criação de receita + bordas; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Em andamento |
| RF-002 | `transaction_service` | criação de despesa + bordas; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Em andamento |
| RF-003 | `transaction_service` | categorização válida/inválida; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` | Em andamento |
| RF-004 | `balance_service` | saldo vazio, positivo e negativo | Planejado |
| RF-005 | `monthly_summary_service` | filtro mensal e mês vazio | Planejado |
| RF-006 | `budget_service` | `test_budget_service.py`, `test_budget_repository_contract.py`, `test_budget_page.py` | Implementado |
| RNF-FIN-001 | `shared.money` | precisão decimal / rejeição de float; `test_money.py`, `test_budget.py` | Implementado |
