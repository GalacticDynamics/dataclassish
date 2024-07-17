"""Extension functions for ``dataclasstools``."""

__all__ = ["field_values", "field_items"]

from collections.abc import Iterator
from typing import Any

from plum import dispatch

from ._core import DataclassInstance, fields


@dispatch  # type: ignore[misc]
def field_values(obj: DataclassInstance) -> Iterator[Any]:
    """Return the values of a dataclass instance."""
    yield from (getattr(obj, f.name) for f in fields(obj))


@dispatch  # type: ignore[misc]
def field_items(obj: DataclassInstance) -> Iterator[tuple[str, Any]]:
    """Return the field names and values of a dataclass instance."""
    yield from ((f.name, getattr(obj, f.name)) for f in fields(obj))
