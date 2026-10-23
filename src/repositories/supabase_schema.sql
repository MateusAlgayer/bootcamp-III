-- Esquema esperado por repositories/supabase_adapter.py (ADR-006).
-- Aplicar no SQL Editor do Supabase ou via migração da CLI.

create table if not exists public.categories (
    id bigint generated always as identity primary key,
    name text not null unique
);

create table if not exists public.transactions (
    id bigint generated always as identity primary key,
    kind text not null check (kind in ('INCOME', 'EXPENSE')),
    -- numeric exato; nunca real/double precision (RNF-FIN-001).
    amount numeric(14, 2) not null check (amount > 0),
    occurred_on date not null,
    description text not null,
    category_id bigint references public.categories (id)
);

create index if not exists transactions_occurred_on_idx
    on public.transactions (occurred_on, id);

-- Sem políticas: a chave anon não lê nem grava. O app usa a service_role no servidor.
alter table public.categories enable row level security;
alter table public.transactions enable row level security;
