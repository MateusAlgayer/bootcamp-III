# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service` | registro de receita + bordas em `test_transaction_service.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-002 | `transaction_service` | registro de despesa + bordas em `test_transaction_service.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Implementado |
| RF-003 | `transaction_service` | categorização válida/inválida em `test_transaction_service.py`; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` | Implementado |
| RF-004 | `balance_service` | saldo vazio, positivo e negativo | Implementado |
| RF-005 | `monthly_summary_service` | filtro mensal e mês vazio | Implementado |
| RF-006 | `budget_service` | orçamento válido/inválido e comparação | Implementado |
| RNF-FIN-001 | `shared.money` | precisão decimal / rejeição de float | Implementado |
