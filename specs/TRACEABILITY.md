# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service` | criação de receita + bordas; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Em andamento |
| RF-002 | `transaction_service` | criação de despesa + bordas; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` | Em andamento |
| RF-003 | `transaction_service` | categorização válida/inválida; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` | Em andamento |
| RF-004 | `balance_service` | saldo vazio, positivo e negativo; precisão decimal; cada transação uma vez em `test_balance_service.py` | Implementado |
| RF-005 | `monthly_summary_service` | filtro mensal e mês vazio | Planejado |
| RF-006 | `budget_service` | orçamento válido/inválido e comparação | Planejado |
| RNF-FIN-001 | `shared.money` | precisão decimal / rejeição de float | Implementado |
