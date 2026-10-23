# ADR-006 — Supabase como banco principal

- **Status:** Proposed
- **Contexto:** a issue #19 previa um adaptador SQLite; a equipe decidiu usar o Supabase
  (Postgres gerenciado) como banco principal. O cliente oficial (`supabase`) acessa as tabelas
  via PostgREST, que serializa `numeric` como número JSON e, portanto, como `float` no Python.
- **Decisão:** implementar os contratos de `repositories/contracts.py` em
  `repositories/supabase_adapter.py`, com o cliente injetado pelo construtor. Valores
  monetários trafegam como texto (`amount::text` na leitura, `str` na escrita) e a coluna é
  `numeric(14, 2)`. O esquema fica em `repositories/supabase_schema.sql`, com RLS habilitado e
  sem políticas; o app usa a chave `service_role` apenas no servidor, lida do ambiente e nunca
  versionada. Erros `APIError`/`httpx.HTTPError` são reencapsulados conforme ADR-004.
- **Consequências:** nova dependência `supabase` (e transitivas); testes usam um cliente mock
  determinístico, sem rede, e o adaptador em memória cobre o mesmo contrato. O comportamento
  real do PostgREST não é exercitado no CI. `AGENTS.md` ainda cita `repositories/sqlite.py`
  como implementação concreta e precisa ser atualizado se esta ADR for aceita.
