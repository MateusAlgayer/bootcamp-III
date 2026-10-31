-- Esquema do banco local SQLite (ADR-007).
-- Criado automaticamente por repositories/sqlite.py no primeiro acesso.

create table if not exists categories (
    id integer primary key autoincrement,
    name text not null unique
);

create table if not exists transactions (
    id integer primary key autoincrement,
    kind text not null check (kind in ('INCOME', 'EXPENSE')),
    -- Centavos inteiros preservam o valor exato sem float (RNF-FIN-001).
    amount_cents integer not null check (amount_cents > 0),
    occurred_on text not null,
    description text not null,
    category_id integer references categories (id)
);

create index if not exists transactions_occurred_on_idx
    on transactions (occurred_on, id);

create table if not exists budgets (
    year integer not null check (year between 1 and 9999),
    month integer not null check (month between 1 and 12),
    limit_cents integer not null check (limit_cents > 0),
    primary key (year, month)
);
