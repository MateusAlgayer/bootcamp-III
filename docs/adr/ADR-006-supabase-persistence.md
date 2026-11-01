# ADR-006 — Supabase como banco principal

- **Status:** Superseded by ADR-007
- **Contexto:** a aplicação precisa de persistência durável em um Postgres gerenciado. O
  cliente oficial (`supabase`) acessa as tabelas via PostgREST, que serializa `numeric` como
  número JSON e, portanto, como `float` no Python.
- **Decisão:** implementar os contratos de `repositories/contracts.py` em
  `repositories/supabase_adapter.py`, com o cliente injetado pelo construtor. Valores
  monetários trafegam como texto (`amount::text` na leitura, `str` na escrita) e a coluna é
  `numeric(14, 2)`. O esquema fica em `repositories/supabase_schema.sql`, com RLS habilitado e
  sem políticas; o app usa a chave `service_role` apenas no servidor, lida do ambiente e nunca
  versionada. Erros `APIError`/`httpx.HTTPError` são reencapsulados conforme ADR-004. Supabase
  é a única persistência definida; o adaptador em memória permanece restrito a testes e ao
  desenvolvimento local.
- **Consequências:** nova dependência `supabase` (e transitivas); testes usam um cliente mock
  determinístico, sem rede, e o adaptador em memória cobre o mesmo contrato. O comportamento
  real do PostgREST não é exercitado no CI. Com a substituição desta decisão pela ADR-007,
  o `AGENTS.md` voltou a apontar `repositories/sqlite.py` como implementação concreta.
