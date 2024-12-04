"""Register dispatches for dataclass objects."""

__all__: list[str] = []

import sys
from collections.abc import Callable, Mapping
from dataclasses import (
    Field,
    asdict as _dataclass_asdict,
    astuple as _dataclass_astuple,
    fields as _dataclass_fields,
    replace as _dataclass_replace,
)
from typing import Any

from plum import dispatch

from .register_base import _recursive_replace_helper
from .types import DataclassInstance

# ===================================================================

if sys.version_info < (3, 13):

    @dispatch  # type: ignore[misc]
    def get_field(obj: DataclassInstance, k: str, /) -> Any:
        """Get a field of a dataclass instance by name.

        Examples
        --------
        >>> from dataclasses import dataclass
        >>> from dataclassish import get_field

        >>> @dataclass
        ... class Point:
        ...     x: float
        ...     y: float

        >>> p = Point(1.0, 2.0)
        >>> get_field(p, "x")
        1.0

        """
        return getattr(obj, k)


# ===================================================================
# Replace

if sys.version_info < (3, 13):

    @dispatch
    def replace(obj: DataclassInstance, /, **kwargs: Any) -> DataclassInstance:
        """Replace the fields of a dataclass instance.

        Examples
        --------
        >>> from dataclasses import dataclass
        >>> from dataclassish import replace

        >>> @dataclass
        ... class Point:
        ...     x: float
        ...     y: float

        >>> p = Point(1.0, 2.0)
        >>> p
        Point(x=1.0, y=2.0)

        >>> replace(p, x=3.0)
        Point(x=3.0, y=2.0)

        """
        return _dataclass_replace(obj, **kwargs)

    @dispatch  # type: ignore[no-redef]
    def replace(obj: DataclassInstance, fs: Mapping[str, Any], /) -> DataclassInstance:
        """Replace the fields of a dataclass instance.

        Examples
        --------
        >>> from dataclasses import dataclass
        >>> from dataclassish import replace, F

        >>> @dataclass
        ... class Point:
        ...     x: float | dict
        ...     y: float

        >>> @dataclass
        ... class TwoPoints:
        ...     a: Point
        ...     b: Point

        >>> p = TwoPoints(Point(1.0, 2.0), Point(3.0, 4.0))
        >>> p
        TwoPoints(a=Point(x=1.0, y=2.0), b=Point(x=3.0, y=4.0))

        >>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
        TwoPoints(a=Point(x=5.0, y=2.0), b=Point(x=3.0, y=6.0))

        >>> replace(p, {"a": {"x": F({"thing": 5.0})}})
        TwoPoints(a=Point(x={'thing': 5.0}, y=2.0),
                    b=Point(x=3.0, y=4.0))

        This also works on mixed-type structures, e.g. a dictionary of dataclasses.

        >>> p = {"a": Point(1.0, 2.0), "b": Point(3.0, 4.0)}
        >>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
        {'a': Point(x=5.0, y=2.0), 'b': Point(x=3.0, y=6.0)}

        Or a dataclass of dictionaries.

        >>> @dataclass
        ... class Object:
        ...     a: dict[str, Any]
        ...     b: dict[str, Any]

        >>> p = Object({"a": 1, "b": 2}, {"c": 3, "d": 4})
        >>> replace(p, {"a": {"b": 5}, "b": {"c": 6}})
        Object(a={'a': 1, 'b': 5}, b={'c': 6, 'd': 4})

        """
        kwargs = {k: _recursive_replace_helper(obj, k, v) for k, v in fs.items()}
        return replace(obj, **kwargs)


# ===================================================================
# Fields


@dispatch  # type: ignore[misc]
def fields(obj: DataclassInstance, /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # TODO: raise issue in beartype
    """Return the fields of a dataclass instance.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import fields

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> fields(p)
    (Field(name='x',type=<class 'float'>,...),
     Field(name='y',type=<class 'float'>,...))

    """
    return _dataclass_fields(obj)


# ===================================================================
# Asdict


@dispatch  # type: ignore[misc]
def asdict(
    obj: DataclassInstance,
    /,
    *,
    dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict,
) -> dict[str, Any]:
    """Return the fields of a dataclass instance as a dictionary.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import asdict

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> asdict(p)
    {'x': 1.0, 'y': 2.0}

    """
    return _dataclass_asdict(obj, dict_factory=dict_factory)


# ===================================================================
# Astuple


@dispatch  # type: ignore[misc]
def astuple(
    obj: DataclassInstance,
    /,
    *,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of a dataclass instance as a tuple.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import astuple

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> astuple(p)
    (1.0, 2.0)

    """
    return _dataclass_astuple(obj, tuple_factory=tuple_factory)
