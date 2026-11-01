# ADR-007 — Persistência local em SQLite com Docker Compose

- **Status:** Accepted
- **Contexto:** o projeto deve rodar sempre localmente, sem depender de serviço gerenciado,
  credenciais externas ou rede. A aplicação é single-user e o volume de dados é pequeno.
  A ADR-006 previa Supabase, mas a operação local e o Docker Compose passaram a ser o modo
  oficial de execução.
- **Decisão:** usar SQLite como única persistência da aplicação. O banco fica em
  `DATABASE_PATH` (padrão `data/finance.db`), criado automaticamente a partir de
  `repositories/sqlite_schema.sql`. Valores monetários são persistidos como centavos inteiros
  (`amount_cents`, `limit_cents`) para preservar exatidão (RNF-FIN-001). O Docker Compose monta
  o volume nomeado `finance-data` em `/app/data`, de modo que os dados sobrevivem a
  `docker compose down`. Os adaptadores em memória permanecem restritos a testes e contratos.
- **Consequências:** não há dependência de rede nem credenciais; o backup é a cópia do arquivo
  SQLite; escritas concorrentes são limitadas pelo modelo single-writer do SQLite; mudanças de
  esquema exigem migração manual/versionada; testes usam bancos temporários via `tmp_path`.
