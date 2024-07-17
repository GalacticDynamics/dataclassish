"""Core module for ``dataclasstools``."""

__all__ = ["DataclassInstance", "replace", "fields", "asdict", "astuple"]

from collections.abc import Callable, Hashable, Mapping
from dataclasses import (
    Field,
    asdict as _dataclass_asdict,
    astuple as _dataclass_astuple,
    field,
    fields as _dataclass_fields,
    replace as _dataclass_replace,
)
from typing import Any, ClassVar, Protocol, runtime_checkable

from plum import dispatch


@runtime_checkable
class DataclassInstance(Protocol):
    """Protocol for dataclass instances."""

    __dataclass_fields__: ClassVar[dict[str, Any]]

    # B/c of https://github.com/python/mypy/issues/3939 just having
    # `__dataclass_fields__` is insufficient for `issubclass` checks.
    @classmethod
    def __subclasshook__(cls: type, c: type) -> bool:
        """Customize the subclass check."""
        return hasattr(c, "__dataclass_fields__")


# ===================================================================
# Replace


@dispatch
def replace(obj: DataclassInstance, /, **kwargs: Any) -> DataclassInstance:
    """Replace the fields of a dataclass instance.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import replace

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
def replace(obj: Mapping[Hashable, Any], /, **kwargs: Any) -> Mapping[Hashable, Any]:
    """Replace the fields of a mapping.

    This operates similarly to `dict.update`, except that
    the kwargs are checked against the keys of the mapping.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import replace

    >>> p = {"a": 1, "b": 2, "c": 3}
    >>> p
    {'a': 1, 'b': 2, 'c': 3}

    >>> replace(p, c=4.0)
    {'a': 1, 'b': 2, 'c': 4.0}

    """
    extra_keys = set(kwargs) - set(obj)
    if extra_keys:
        msg = f"invalid keys {extra_keys}."
        raise ValueError(msg)

    return type(obj)(**{**obj, **kwargs})


# ===================================================================
# Fields


@dispatch
def fields(obj: DataclassInstance, /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # TODO: raise issue in beartype
    """Return the fields of a dataclass instance.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import fields

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


@dispatch  # type: ignore[no-redef]
def fields(obj: Mapping[str, Any], /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # TODO: raise issue in beartype
    """Return the mapping as a tuple of `dataclass.Field` objects.

    Examples
    --------
    >>> from dataclasstools import fields

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> fields(p)
    (Field(name='a',type=<class 'int'>,...),
     Field(name='b',type=<class 'float'>,...),
     Field(name='c',type=<class 'str'>,...))

    """
    fs = tuple(field(kw_only=True) for _ in obj)  # pylint: disable=invalid-field-call
    for f, (k, v) in zip(fs, obj.items(), strict=True):
        f.name = k
        f.type = type(v)
    return fs


# ===================================================================
# Asdict


@dispatch
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
    >>> from dataclasstools import asdict

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> asdict(p)
    {'x': 1.0, 'y': 2.0}

    """
    return _dataclass_asdict(obj, dict_factory=dict_factory)


@dispatch  # type: ignore[no-redef]
def asdict(
    obj: Mapping[str, Any],
    /,
    *,
    dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict,
) -> dict[str, Any]:
    """Return the fields of a mapping as a dictionary.

    Following the `asdict` API, the dictionary may be copied if ``dict_factory``
    performs a copy when constructed from a :class:`~collections.abc.Mapping`.

    Examples
    --------
    >>> from dataclasstools import asdict

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> asdict(p)
    {'a': 1, 'b': 2.0, 'c': '3'}

    >>> asdict(p) is p
    False

    """
    return dict_factory(obj)


# ===================================================================
# Astuple


@dispatch
def astuple(
    obj: DataclassInstance,
    /,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of a dataclass instance as a tuple.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclasstools import astuple

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> astuple(p)
    (1.0, 2.0)

    """
    return _dataclass_astuple(obj, tuple_factory=tuple_factory)


@dispatch  # type: ignore[no-redef]
def astuple(
    obj: Mapping[str, Any],
    /,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of a mapping as a tuple.

    Examples
    --------
    >>> from dataclasstools import astuple

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> astuple(p)
    (1, 2.0, '3')

    """
    return tuple_factory(obj.values())
