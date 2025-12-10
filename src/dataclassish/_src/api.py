"""API for functions in Dataclassish."""

# pylint: disable=duplicate-code
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
# pylint: enable=duplicate-code

from collections.abc import Callable, Hashable
from dataclasses import Field
from typing import Any, TypeAlias

from plum import dispatch

# ============================================================================
# Dataclass API


@dispatch.abstract
def replace(obj: Any, /, **kwargs: Any) -> Any:
    """Replace the fields of an object.

    Args:
        obj: The object whose fields should be replaced.
        **kwargs: Field names and their new values.

    Returns:
        A new object with the specified fields replaced.

    """
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def fields(obj: Any, /) -> tuple[Field, ...]:  # type: ignore[type-arg]
    """Return the fields of an object.

    Args:
        obj: The object whose fields to retrieve.

    Returns:
        A tuple of Field objects describing the object's fields.

    """
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
    """Get the value of a field from an object.

    Args:
        obj: The object from which to get the field.
        field_name: The name of the field to retrieve.

    Returns:
        The value of the specified field.

    """
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_keys(obj: Any, /) -> tuple[str, ...]:
    """Return the field names from the `dataclassish.fields`.

    Args:
        obj: The object whose field names to retrieve.

    Returns:
        A tuple of field names.

    """
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_values(obj: Any, /) -> tuple[Any, ...]:
    """Return the field values from the `dataclassish.fields`.

    Args:
        obj: The object whose field values to retrieve.

    Returns:
        A tuple of field values.

    """
    raise NotImplementedError  # pragma: no cover


@dispatch.abstract
def field_items(obj: Any, /) -> tuple[tuple[str, Any], ...]:
    """Return the field items from the `dataclassish.fields`.

    Args:
        obj: The object whose field items to retrieve.

    Returns:
        A tuple of (field_name, field_value) pairs.

    """
    raise NotImplementedError  # pragma: no cover
