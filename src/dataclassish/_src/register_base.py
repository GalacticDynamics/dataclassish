"""Register dispatches for objects."""

__all__: list[str] = []

from typing import Any, TypeVar

from plum import dispatch

from .api import fields

K = TypeVar("K")
V = TypeVar("V")


# ===================================================================
# Field keys


@dispatch  # type: ignore[misc]
def field_keys(obj: Any, /) -> tuple[str, ...]:
    """Yield the field names from the `dataclassish.fields`.

    Examples
    --------
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


@dispatch  # type: ignore[misc]
def field_values(obj: Any, /) -> tuple[Any, ...]:
    """Return the field values from the `dataclassish.fields`.

    Examples
    --------
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


@dispatch  # type: ignore[misc]
def field_items(obj: Any) -> tuple[tuple[str, Any], ...]:
    """Return the field names and values from the `dataclassish.fields`.

    Examples
    --------
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
