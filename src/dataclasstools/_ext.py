"""Extension functions for ``dataclasstools``."""

__all__ = ["field_keys", "field_values", "field_items"]

from collections.abc import Hashable, Iterator, Mapping
from typing import Any, TypeVar

from plum import dispatch

from ._core import fields

K = TypeVar("K")
V = TypeVar("V")

# ===================================================================
# Field keys


@dispatch
def field_keys(obj: Any, /) -> Iterator[str]:
    """Yield the field names from the `dataclasstools.fields`.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import field_keys

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> list(field_keys(p))
    ['x', 'y']

    """
    yield from (f.name for f in fields(obj))


@dispatch  # type: ignore[no-redef]
# TODO: def field_keys(obj: Mapping[K, V]) -> Iterator[K]:
def field_keys(obj: Mapping[Hashable, Any]) -> Iterator[Hashable]:
    """Return the keys of a mapping.

    Examples
    --------
    >>> from dataclasstools import field_keys

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> list(field_keys(p))
    ['a', 'b', 'c']

    """
    yield from obj.keys()


# ===================================================================
# Field values


@dispatch
def field_values(obj: Any, /) -> Iterator[Any]:
    """Yield the field values from the `dataclasstools.fields`.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import field_values

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> list(field_values(p))
    [1.0, 2.0]

    """
    yield from (getattr(obj, f.name) for f in fields(obj))


@dispatch  # type: ignore[no-redef]
# TODO: def field_values(obj: Mapping[Any, V]) -> Iterator[V]:
def field_values(obj: Mapping[Any, Any]) -> Iterator[Any]:
    """Return the values of a mapping.

    Examples
    --------
    >>> from dataclasstools import field_values

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> list(field_values(p))
    [1, 2.0, '3']

    """
    yield from obj.values()


# ===================================================================
# Field items


@dispatch
def field_items(obj: Any) -> Iterator[tuple[str, Any]]:
    """Yield the field names and values from the `dataclasstools.fields`.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import field_items

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> list(field_items(p))
    [('x', 1.0), ('y', 2.0)]

    """
    yield from ((f.name, getattr(obj, f.name)) for f in fields(obj))


@dispatch  # type: ignore[no-redef]
# TODO: def field_items(obj: Mapping[K, V]) -> Iterator[tuple[K, V]]:
def field_items(obj: Mapping[Any, Any]) -> Iterator[tuple[Any, Any]]:
    """Return the items of a mapping.

    Examples
    --------
    >>> from dataclasstools import field_items

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> list(field_items(p))
    [('a', 1), ('b', 2.0), ('c', '3')]

    """
    yield from obj.items()
