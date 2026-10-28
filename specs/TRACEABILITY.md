# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service`, `transaction_controller` | registro de receita + bordas em `test_transaction_service.py` e `test_transaction_controller.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-002 | `transaction_service`, `transaction_controller` | registro de despesa + bordas em `test_transaction_service.py` e `test_transaction_controller.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-003 | `transaction_service`, `transaction_controller` | categorização válida/inválida em `test_transaction_service.py` e `test_transaction_controller.py`; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` | Implementado |
| RF-004 | `balance_service`, `dashboard_controller` | `test_balance_service.py`, `test_dashboard_controller.py`; consistência em `test_monthly_summary_service.py` | Implementado |
| RF-005 | `monthly_summary_service`, `dashboard_controller` | `test_monthly_summary_service.py`, `test_monthly_summary.py`, `test_dashboard_controller.py`, `test_dashboard_page.py` | Implementado |
| RF-006 | `budget_service`, `budget_controller` | `test_budget_service.py`, `test_budget_controller.py`, `test_budget_repository_contract.py`, `test_budget_page.py` | Implementado |
| RNF-FIN-001 | `shared.money` | precisão decimal / rejeição de float; `test_money.py`, `test_budget.py` | Implementado |
