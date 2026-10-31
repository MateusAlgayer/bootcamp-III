# Matriz de Rastreabilidade

| Requisito | Unidade principal | Teste planejado | Estado |
|---|---|---|---|
| RF-001 | `transaction_service`, `transaction_controller`, `sqlite_transaction_repository` | registro de receita + bordas em `test_transaction_service.py` e `test_transaction_controller.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` (memória e SQLite); view em `test_transactions_page.py` | Implementado |
| RF-002 | `transaction_service`, `transaction_controller`, `sqlite_transaction_repository` | registro de despesa + bordas em `test_transaction_service.py` e `test_transaction_controller.py`; entidade em `test_transaction.py`; recuperação em `test_transaction_repository_contract.py` (memória e SQLite); view em `test_transactions_page.py` | Implementado |
| RF-003 | `transaction_service`, `transaction_controller`, `sqlite_transaction_repository` | categorização válida/inválida em `test_transaction_service.py` e `test_transaction_controller.py`; imutabilidade em `test_transaction.py`; persistência em `test_transaction_repository_contract.py` (memória e SQLite); view em `test_transactions_page.py` | Implementado |
| RF-004 | `balance_service`, `dashboard_controller` | `test_balance_service.py`, `test_dashboard_controller.py`; consistência em `test_monthly_summary_service.py` | Implementado no domínio/controller; sem tela dedicada |
| RF-005 | `monthly_summary_service`, `dashboard_controller` | `test_monthly_summary_service.py`, `test_monthly_summary.py`, `test_dashboard_controller.py`, `test_dashboard_page.py` | Implementado |
| RF-006 | `budget_service`, `budget_controller`, `sqlite_budget_repository` | `test_budget_service.py`, `test_budget_controller.py`, `test_budget_repository_contract.py` (memória e SQLite), `test_budget_page.py` | Implementado |
| RNF-FIN-001 | `shared.money`, `sqlite` | precisão decimal / centavos inteiros / rejeição de float; `test_money.py`, `test_budget.py`, `test_sqlite_adapter.py` | Implementado |
| RNF-TEST-001 | `test/unit`, `test/integration` | testes unitários sem Streamlit; UI exercitada com `streamlit.testing.v1.AppTest` | Implementado |
| RNF-SDD-001 | `specs/TRACEABILITY.md`, `specs/CHANGELOG.md` | cada RF referencia teste e estado; mudanças registradas no changelog | Implementado |
| RNF-AI-001 | `AGENTS.md`, ADR-003 | revisão por agente com gates determinísticos e merge humano | Em processo |

## Pendências

As pendências de implementação estão detalhadas na seção 5.1 da
[SPEC-001](SPEC-001-financial-control.md): categorias iniciais sem CRUD, RF-004 sem tela
dedicada e migrações de esquema manuais. A persistência é SQLite local (ADR-007); a ADR-006
(Supabase) foi substituída.
