"""Erros de domínio e aplicação compartilhados (ADR-004)."""


class DomainError(Exception):
    """Raiz das falhas previstas pela aplicação."""


class ValidationError(DomainError):
    """Entrada viola uma regra de domínio."""


class NotFoundError(DomainError):
    """Recurso solicitado não existe no escopo informado."""


class ConflictError(DomainError):
    """Operação conflita com um recurso já existente."""
