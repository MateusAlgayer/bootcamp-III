"""Caso de uso de cálculo de saldo consolidado (RF-004)."""

from collections.abc import Iterable
from decimal import Decimal

from models.transaction import Transaction, TransactionType
from repositories.contracts import TransactionRepository
from shared.money import quantize_money


def sum_by_kind(transactions: Iterable[Transaction]) -> tuple[Decimal, Decimal]:
    """Soma receitas e despesas separadamente, na ordem em que forem recebidas."""
    income = Decimal(0)
    expenses = Decimal(0)
    for transaction in transactions:
        if transaction.kind is TransactionType.INCOME:
            income += transaction.amount
        else:
            expenses += transaction.amount
    return quantize_money(income), quantize_money(expenses)


def calculate_balance(transactions: Iterable[Transaction]) -> Decimal:
    """Calcula ``receitas - despesas`` para as transações informadas (RF-004)."""
    income, expenses = sum_by_kind(transactions)
    return quantize_money(income - expenses)


class BalanceService:
    """Calcula o saldo consolidado de todas as transações persistidas."""

    def __init__(self, repository: TransactionRepository) -> None:
        self._repository = repository

    def calculate(self) -> Decimal:
        """Retorna o saldo consolidado como receitas menos despesas (RF-004)."""
        return calculate_balance(self._repository.list_all())
