"""Register dispatches for objects."""

__all__: tuple[str, ...] = ()

from collections.abc import Mapping
from typing import Any, TypeVar

from plum import dispatch

from .api import fields, replace
from .types import F

# pylint: disable=duplicate-code

K = TypeVar("K")
V = TypeVar("V")

# ===================================================================


@dispatch
def get_field(obj: Any, k: str, /) -> Any:
    """Get a field of an object by name.

    This default implementation is just to call `getattr`.

    Args:
        obj: The object from which to get the field.
        k: The name of the field to retrieve.

    Returns:
        The value of the specified field.

    Examples:
        >>> from dataclassish import get_field

        >>> class Point:
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y

        >>> p = Point(1.0, 2.0)
        >>> get_field(p, "x")
        1.0

    """
    return getattr(obj, k)


# ===================================================================
# Replace


def _recursive_replace_helper(obj: object, k: str, v: Any, /) -> Any:
    if isinstance(v, F):
        out = v.value
    elif isinstance(v, Mapping):
        out = replace(get_field(obj, k), v)
    else:
        out = v
    return out


# ===================================================================
# Field keys


@dispatch
def field_keys(obj: Any, /) -> tuple[str, ...]:
    """Yield the field names from the `dataclassish.fields`.

    Args:
        obj: The object whose field names to retrieve.

    Returns:
        A tuple of field names.

    Examples:
        >>> from dataclasses import dataclass
        >>> from dataclassish import field_keys

        >>> @dataclass
        ... class Point:
        ...     x: float
        ...     y: float

        >>> p = Point(1.0, 2.0)
        >>> field_keys(p)
        ('x', 'y')

    """
    return tuple(f.name for f in fields(obj))


# ===================================================================
# Field values


@dispatch
def field_values(obj: Any, /) -> tuple[Any, ...]:
    """Return the field values from the `dataclassish.fields`.

    Args:
        obj: The object whose field values to retrieve.

    Returns:
        A tuple of field values.

    Examples:
        >>> from dataclasses import dataclass
        >>> from dataclassish import field_values

        >>> @dataclass
        ... class Point:
        ...     x: float
        ...     y: float

        >>> p = Point(1.0, 2.0)
    >>> field_values(p)
    (1.0, 2.0)

    """
    return tuple(getattr(obj, f.name) for f in fields(obj))


# ===================================================================
# Field items


@dispatch
def field_items(obj: Any) -> tuple[tuple[str, Any], ...]:
    """Return the field names and values from the `dataclassish.fields`.

    Args:
        obj: The object whose field items to retrieve.

    Returns:
        A tuple of (field_name, field_value) pairs.

    Examples:
        >>> from dataclasses import dataclass
        >>> from dataclassish import field_items

        >>> @dataclass
        ... class Point:
        ...     x: float
        ...     y: float

        >>> p = Point(1.0, 2.0)
        >>> field_items(p)
        (('x', 1.0), ('y', 2.0))

    """
    return tuple((f.name, getattr(obj, f.name)) for f in fields(obj))
