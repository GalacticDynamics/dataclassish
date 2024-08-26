"""Extension functions for ``dataclassish``."""

__all__ = ["field_keys", "field_values", "field_items"]

from collections.abc import Hashable, ItemsView, KeysView, Mapping, ValuesView
from typing import Any, TypeVar

from plum import dispatch

from ._core import fields

K = TypeVar("K")
V = TypeVar("V")


# ===================================================================
# Field keys


@dispatch
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


@dispatch  # type: ignore[no-redef]
def field_keys(obj: Mapping[Hashable, Any]) -> KeysView[Hashable]:
    """Return the keys of a mapping.

    Examples
    --------
    >>> from dataclassish import field_keys

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_keys(p)
    dict_keys(['a', 'b', 'c'])

    """
    return obj.keys()


# ===================================================================
# Field values


@dispatch
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


@dispatch  # type: ignore[no-redef]
def field_values(obj: Mapping[Any, Any]) -> ValuesView[Any]:
    """Return the values of a mapping.

    Examples
    --------
    >>> from dataclassish import field_values

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_values(p)
    dict_values([1, 2.0, '3'])

    """
    return obj.values()


# ===================================================================
# Field items


@dispatch
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


@dispatch  # type: ignore[no-redef]
def field_items(obj: Mapping[Any, Any]) -> ItemsView[Any, Any]:
    """Return the items of a mapping.

    Examples
    --------
    >>> from dataclassish import field_items

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_items(p)
    dict_items([('a', 1), ('b', 2.0), ('c', '3')])

    """
    return obj.items()
