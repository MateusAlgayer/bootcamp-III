"""Testes unitários da hierarquia de erros de domínio (ADR-004)."""

import pytest

from shared.errors import ConflictError, DomainError, NotFoundError, ValidationError

_SUBTYPES: list[type[DomainError]] = [ValidationError, NotFoundError, ConflictError]


@pytest.mark.unit
def test_domain_error_is_exception_root() -> None:
    assert issubclass(DomainError, Exception)


@pytest.mark.unit
@pytest.mark.parametrize("error_type", _SUBTYPES)
def test_subtype_inherits_from_domain_error(error_type: type[DomainError]) -> None:
    assert issubclass(error_type, DomainError)


@pytest.mark.unit
@pytest.mark.parametrize("error_type", _SUBTYPES)
def test_subtype_caught_by_root_when_raised(error_type: type[DomainError]) -> None:
    with pytest.raises(DomainError):
        raise error_type("regra violada")


@pytest.mark.unit
@pytest.mark.parametrize("error_type", _SUBTYPES)
def test_subtype_preserves_message_when_raised(error_type: type[DomainError]) -> None:
    message = "valor deve ser positivo (RF-001)"

    with pytest.raises(error_type) as exc_info:
        raise error_type(message)

    assert str(exc_info.value) == message


@pytest.mark.unit
@pytest.mark.parametrize(
    ("error_type", "other_type"),
    [
        (error_type, other_type)
        for error_type in _SUBTYPES
        for other_type in _SUBTYPES
        if error_type is not other_type
    ],
)
def test_subtype_not_subclass_of_sibling_when_distinct(
    error_type: type[DomainError], other_type: type[DomainError]
) -> None:
    assert not issubclass(error_type, other_type)
