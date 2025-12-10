"""API for functions in Dataclassish."""

__all__ = (
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
)

from collections.abc import Callable, Hashable
from dataclasses import Field
from typing import Any, TypeAlias

from plum import dispatch

# ============================================================================
# Dataclass API


@dispatch.abstract
def replace(obj: Any, /, **kwargs: Any) -> Any:
    """Replace the fields of an object."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def fields(obj: Any, /) -> tuple[Field, ...]:  # type: ignore[type-arg]
    """Return the fields of an object."""
    raise NotImplementedError  # pragma: no cover


DictFactory: TypeAlias = Callable[[list[tuple[str, Any]]], dict[str, Any]]


@dispatch.abstract
def asdict(obj: Any, /, *, dict_factory: DictFactory = dict) -> dict[Hashable, Any]:
    """Return the fields of an object as a dictionary.

    Args:
        obj: The object to convert to a dictionary.
        dict_factory: Factory function to create the dictionary.

    Returns:
        A dictionary mapping field names to their values.

    """
    raise NotImplementedError  # pragma: no cover


TupleFactory: TypeAlias = Callable[[list[Any]], tuple[Any, ...]]


@dispatch.abstract
def astuple(obj: Any, /, tuple_factory: TupleFactory = tuple) -> tuple[Any, ...]:
    """Return the fields of an object as a tuple.

    Args:
        obj: The object to convert to a tuple.
        tuple_factory: Factory function to create the tuple.

    Returns:
        A tuple containing the object's field values.

    """
    raise NotImplementedError  # pragma: no cover


# ============================================================================
# Extensions


@dispatch.abstract
def get_field(obj: Any, field_name: str, /) -> Any:
    """Get the value of a field from an object."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_keys(obj: Any, /) -> tuple[str, ...]:
    """Return the field names from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_values(obj: Any, /) -> tuple[Any, ...]:
    """Return the field values from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_items(obj: Any, /) -> tuple[tuple[str, Any], ...]:
    """Return the field items from the `dataclassish.fields`."""
    raise NotImplementedError  # pragma: no cover
