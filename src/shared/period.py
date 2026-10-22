"""Período mensal (ano/mês) usado pelos casos de uso financeiros."""

from dataclasses import dataclass
from datetime import date

from shared.errors import ValidationError

MIN_YEAR = 1
MAX_YEAR = 9999


@dataclass(frozen=True, slots=True)
class YearMonth:
    """Mês de competência, imutável e utilizável como chave de dicionário."""

    year: int
    month: int

    def __post_init__(self) -> None:
        if isinstance(self.year, bool) or not isinstance(self.year, int):
            raise ValidationError("ano deve ser um inteiro")
        if isinstance(self.month, bool) or not isinstance(self.month, int):
            raise ValidationError("mês deve ser um inteiro")
        if not MIN_YEAR <= self.year <= MAX_YEAR:
            raise ValidationError(f"ano deve estar entre {MIN_YEAR} e {MAX_YEAR}")
        if not 1 <= self.month <= 12:
            raise ValidationError("mês deve estar entre 1 e 12")

    @classmethod
    def from_date(cls, value: date) -> "YearMonth":
        """Extrai o período mensal de uma data."""
        return cls(year=value.year, month=value.month)

    def label(self) -> str:
        """Representação legível no formato ``MM/AAAA``."""
        return f"{self.month:02d}/{self.year}"
