"""Entidade de domínio para transações financeiras"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum

from shared.errors import ValidationError
from shared.money import InvalidMoneyValueError, Money


class TransactionType(StrEnum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


@dataclass(frozen=True, slots=True)
class Transaction:
    kind: TransactionType
    amount: Decimal
    occurred_on: date
    description: str
    category_id: int | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, TransactionType):
            raise ValidationError(
                "tipo da transação deve ser INCOME ou EXPENSE (RF-001, RF-002)"
            )
        # datetime herda de date, mas comparar datetime com date levanta TypeError.
        if not isinstance(self.occurred_on, date) or isinstance(
            self.occurred_on, datetime
        ):
            raise ValidationError("data da transação deve ser uma data válida")
        object.__setattr__(self, "amount", self._validated_amount())

    def _validated_amount(self) -> Money:
        try:
            amount = Money(self.amount).quantize_cents(ROUND_HALF_UP)
        except InvalidMoneyValueError as exc:
            raise ValidationError(
                "valor da transação deve ser decimal exato, sem float (RNF-FIN-001)"
            ) from exc
        if amount <= 0:
            raise ValidationError(
                "valor da transação deve ser maior que zero (RF-001, RF-002)"
            )
        return amount
