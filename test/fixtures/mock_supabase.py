"""Cliente Supabase mock e determinístico para testes, sem rede."""

from decimal import Decimal
from typing import Any

from postgrest.exceptions import APIError


class MockResponse:
    def __init__(self, data: list[dict[str, Any]]) -> None:
        self.data = data


class _Query:
    def __init__(self, client: "MockSupabaseClient", table: str) -> None:
        self._client = client
        self._table = table
        self._op = "select"
        self._columns = "*"
        self._payload: dict[str, Any] = {}
        self._filters: list[tuple[str, Any]] = []
        self._orders: list[str] = []

    def select(self, columns: str) -> "_Query":
        self._op, self._columns = "select", columns
        return self

    def insert(self, row: dict[str, Any]) -> "_Query":
        self._op, self._payload = "insert", dict(row)
        return self

    def update(self, values: dict[str, Any]) -> "_Query":
        self._op, self._payload = "update", dict(values)
        return self

    def eq(self, column: str, value: Any) -> "_Query":
        self._filters.append((column, value))
        return self

    def order(self, column: str) -> "_Query":
        self._orders.append(column)
        return self

    def execute(self) -> MockResponse:
        if self._client.error is not None:
            raise self._client.error
        rows = self._client.tables.setdefault(self._table, [])
        if self._op == "insert":
            self._check_foreign_key()
            row = {"id": max((r["id"] for r in rows), default=0) + 1, **self._payload}
            if "amount" in row:
                row["amount"] = Decimal(row["amount"])
            rows.append(row)
            return MockResponse([self._render(row)])
        matched = [r for r in rows if all(r[c] == v for c, v in self._filters)]
        if self._op == "update":
            self._check_foreign_key()
            for row in matched:
                row.update(self._payload)
        for column in reversed(self._orders):
            matched.sort(key=lambda r: r[column])
        return MockResponse([self._render(r) for r in matched])

    def _check_foreign_key(self) -> None:
        category_id = self._payload.get("category_id")
        categories = self._client.tables.get("categories", [])
        if category_id is not None and all(c["id"] != category_id for c in categories):
            raise APIError({"code": "23503", "message": "violates foreign key"})

    def _render(self, row: dict[str, Any]) -> dict[str, Any]:
        rendered = dict(row)
        if "amount" in rendered:
            # Igual ao PostgREST: numeric vira número JSON (float) sem o cast ::text.
            as_text = "amount::text" in self._columns
            amount = rendered["amount"]
            rendered["amount"] = str(amount) if as_text else float(amount)
        return rendered


class MockSupabaseClient:
    def __init__(self, categories: tuple[tuple[int, str], ...] = ()) -> None:
        self.tables: dict[str, list[dict[str, Any]]] = {
            "categories": [{"id": i, "name": n} for i, n in categories],
            "transactions": [],
        }
        self.error: Exception | None = None

    def table(self, name: str) -> _Query:
        return _Query(self, name)
