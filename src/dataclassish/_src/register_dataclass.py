"""Register dispatches for dataclass objects."""

__all__: list[str] = []

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

from .types import DataclassInstance, F

# ===================================================================
# Replace


@dispatch  # type: ignore[misc]
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


def _recursive_replace_dataclass_helper(
    obj: DataclassInstance, k: str, v: Any, /
) -> Any:
    if isinstance(v, F):
        out = v.value
    elif isinstance(v, Mapping):
        out = replace(getattr(obj, k), v)
    else:
        out = v
    return out


@dispatch  # type: ignore[misc, no-redef]
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
    ... class PointofPoints:
    ...     a: Point
    ...     b: Point

    >>> p = PointofPoints(Point(1.0, 2.0), Point(3.0, 4.0))
    >>> p
    PointofPoints(a=Point(x=1.0, y=2.0), b=Point(x=3.0, y=4.0))

    >>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
    PointofPoints(a=Point(x=5.0, y=2.0), b=Point(x=3.0, y=6.0))

    >>> replace(p, {"a": {"x": F({"thing": 5.0})}})
    PointofPoints(a=Point(x={'thing': 5.0}, y=2.0),
                  b=Point(x=3.0, y=4.0))

    """
    kwargs = {k: _recursive_replace_dataclass_helper(obj, k, v) for k, v in fs.items()}
    return _dataclass_replace(obj, **kwargs)


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
