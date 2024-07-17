"""Core module for ``dataclasstools``."""

__all__ = ["DataclassInstance", "replace", "fields", "asdict", "astuple"]

from collections.abc import Callable
from dataclasses import Field as _dataclass_Field
from dataclasses import asdict as _dataclass_asdict
from dataclasses import astuple as _dataclass_astuple
from dataclasses import fields as _dataclass_fields
from dataclasses import replace as _dataclass_replace
from typing import Any, ClassVar, Protocol, runtime_checkable

from plum import dispatch


@runtime_checkable
class DataclassInstance(Protocol):
    """Protocol for dataclass instances."""

    __dataclass_fields__: ClassVar[dict[str, Any]]

    # B/c of https://github.com/python/mypy/issues/3939 just having
    # `__dataclass_fields__` is insufficient for `issubclass` checks.
    @classmethod
    def __subclasshook__(cls: type, c: type) -> bool:
        """Customize the subclass check."""
        return hasattr(c, "__dataclass_fields__")


@dispatch  # type: ignore[misc]
def replace(obj: DataclassInstance, /, **kwargs: Any) -> DataclassInstance:
    """Replace the fields of a dataclass instance."""
    return _dataclass_replace(obj, **kwargs)


@dispatch  # type: ignore[misc]
def fields(obj: DataclassInstance) -> tuple[_dataclass_Field[Any], ...]:
    """Return the fields of a dataclass instance."""
    return _dataclass_fields(obj)


@dispatch  # type: ignore[misc]
def asdict(
    obj: DataclassInstance,
    /,
    *,
    dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict,
) -> dict[str, Any]:
    """Return the fields of a dataclass instance as a dictionary."""
    return _dataclass_asdict(obj, dict_factory=dict_factory)


@dispatch  # type: ignore[misc]
def astuple(
    obj: DataclassInstance,
    /,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of a dataclass instance as a tuple."""
    return _dataclass_astuple(obj, tuple_factory=tuple_factory)
