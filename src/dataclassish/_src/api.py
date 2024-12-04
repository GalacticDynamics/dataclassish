"""API for functions in Dataclassish."""

__all__ = [
    # Dataclass API
    "replace",
    "fields",
    "asdict",
    "astuple",
    # Extensions
    "get_field",
    "field_keys",
    "field_values",
    "field_items",
]

from collections.abc import Hashable
from dataclasses import Field
from typing import Any

from plum import dispatch

# ============================================================================
# Dataclass API


@dispatch.abstract  # type: ignore[misc]
def replace(obj: Any, /, **kwargs: Any) -> Any:
    """Replace the fields of an object."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def fields(obj: Any, /) -> tuple[Field, ...]:  # type: ignore[type-arg]
    """Return the fields of an object."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def asdict(obj: Any, /) -> dict[Hashable, Any]:
    """Return the fields of an object as a dictionary."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def astuple(obj: Any, /) -> tuple[Any, ...]:
    """Return the fields of an object as a tuple."""
    raise NotImplementedError  # pragma: no cover


# ============================================================================
# Extensions


@dispatch.abstract  # type: ignore[misc]
def get_field(obj: Any, field_name: str, /) -> Any:
    """Get the value of a field from an object."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def field_keys(obj: Any, /) -> tuple[str, ...]:
    """Return the field names from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def field_values(obj: Any, /) -> tuple[Any, ...]:
    """Return the field values from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract  # type: ignore[misc]
def field_items(obj: Any) -> tuple[tuple[str, Any], ...]:
    """Return the field items from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover
