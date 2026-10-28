"""Caso de uso de cálculo de saldo consolidado (RF-004)."""

from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal

from models.transaction import Transaction, TransactionType
from repositories.contracts import TransactionRepository

MONEY_QUANTUM = Decimal("0.01")


def _quantize(value: Decimal) -> Decimal:
    """Normaliza um total monetário para duas casas com arredondamento explícito."""
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def sum_by_kind(transactions: Iterable[Transaction]) -> tuple[Decimal, Decimal]:
    """Soma receitas e despesas separadamente, na ordem em que forem recebidas."""
    income = Decimal("0.00")
    expenses = Decimal("0.00")
    for transaction in transactions:
        if transaction.kind is TransactionType.INCOME:
            income += transaction.amount
        else:
            expenses += transaction.amount
    return _quantize(income), _quantize(expenses)


def calculate_balance(transactions: Iterable[Transaction]) -> Decimal:
    """Calcula ``receitas - despesas`` para as transações informadas (RF-004)."""
    income, expenses = sum_by_kind(transactions)
    return _quantize(income - expenses)


class BalanceService:
    """Calcula o saldo consolidado de todas as transações persistidas."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    def calculate(self) -> Decimal:
        """Retorna o saldo consolidado como receitas menos despesas (RF-004)."""
        return calculate_balance(self._repository.list_all())
