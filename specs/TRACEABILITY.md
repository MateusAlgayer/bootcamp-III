# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service` | registro de receita + bordas em `test_transaction_service.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-002 | `transaction_service` | registro de despesa + bordas em `test_transaction_service.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-003 | `transaction_service` | categorização válida/inválida em `test_transaction_service.py`; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` | Implementado |
| RF-004 | `balance_service` | `test_balance_service.py`; consistência em `test_monthly_summary_service.py` | Implementado |
| RF-005 | `monthly_summary_service` | `test_monthly_summary_service.py`, `test_monthly_summary.py`, `test_dashboard_controller.py`, `test_dashboard_page.py` | Implementado |
| RF-006 | `budget_service` | `test_budget_service.py`, `test_budget_repository_contract.py`, `test_budget_page.py` | Implementado |
| RNF-FIN-001 | `shared.money` | precisão decimal / rejeição de float; `test_money.py`, `test_budget.py` | Implementado |
