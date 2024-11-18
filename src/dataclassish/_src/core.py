"""Core module for ``dataclassish``."""

__all__ = ["DataclassInstance", "replace", "fields", "asdict", "astuple", "F"]

from collections.abc import Callable, Hashable, Mapping
from dataclasses import (
    Field,
    asdict as _dataclass_asdict,
    astuple as _dataclass_astuple,
    dataclass,
    field,
    fields as _dataclass_fields,
    replace as _dataclass_replace,
)
from typing import Any, ClassVar, Generic, Protocol, TypeVar, runtime_checkable

from plum import dispatch

V = TypeVar("V")


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


@dataclass(frozen=True, slots=True)
class F(Generic[V]):
    """Mark a field as a dataclass field when doing multi-level replacement.

    Examples
    --------
    >>> from dataclassish import F

    >>> F(1)
    F(value=1)

    >>> p = {"a": 1, "b": 2.0, "c": {"aa": 3, "bb": 4}}
    >>> replace(p, {"c": {"aa": 6}})
    {'a': 1, 'b': 2.0, 'c': {'aa': 6, 'bb': 4}}

    >>> from plum import NotFoundLookupError
    >>> try: replace(p, {"c": {"aa": 6, "bb": {"d": 7}}})
    ... except NotFoundLookupError as e: print(e)
    `replace(4, {'d': 7})` could not be resolved...

    >>> replace(p, {"c": F({"aa": 6, "bb": {"d": 7}})})
    {'a': 1, 'b': 2.0, 'c': {'aa': 6, 'bb': {'d': 7}}}

    """

    value: V


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


@dispatch  # type: ignore[no-redef]
def replace(obj: Mapping[Hashable, Any], /, **kwargs: Any) -> Mapping[Hashable, Any]:
    """Replace the fields of a mapping.

    This operates similarly to `dict.update`, except that
    the kwargs are checked against the keys of the mapping.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import replace

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


def _recursive_replace_mapping_helper(
    obj: Mapping[Hashable, Any], k: str, v: Any, /
) -> Any:
    if isinstance(v, F):
        out = v.value
    elif isinstance(v, Mapping):
        out = replace(obj[k], v)
    else:
        out = v
    return out


@dispatch  # type: ignore[misc,no-redef]
def replace(
    obj: Mapping[Hashable, Any], fs: Mapping[str, Any], /
) -> Mapping[Hashable, Any]:
    """Replace the fields of a mapping.

    Examples
    --------
    >>> from dataclassish import replace, F

    >>> p = {"a": 1, "b": 2.0, "c": {"aa": 3, "bb": 4}}
    >>> replace(p, {"c": {"aa": 6}})
    {'a': 1, 'b': 2.0, 'c': {'aa': 6, 'bb': 4}}

    >>> from plum import NotFoundLookupError
    >>> try: replace(p, {"c": {"aa": 6, "bb": {"d": 7}}})
    ... except NotFoundLookupError as e: print(e)
    `replace(4, {'d': 7})` could not be resolved...

    >>> replace(p, {"c": F({"aa": 6, "bb": {"d": 7}})})
    {'a': 1, 'b': 2.0, 'c': {'aa': 6, 'bb': {'d': 7}}}

    """
    # Recursively replace the fields
    kwargs = {k: _recursive_replace_mapping_helper(obj, k, v) for k, v in fs.items()}

    return type(obj)(**(dict(obj) | kwargs))


# ===================================================================
# Fields


@dispatch
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


@dispatch  # type: ignore[no-redef]
def fields(obj: Mapping[str, Any], /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # TODO: raise issue in beartype
    """Return the mapping as a tuple of `dataclass.Field` objects.

    Examples
    --------
    >>> from dataclassish import fields

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
    >>> from dataclassish import asdict

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


@dispatch  # type: ignore[no-redef]
def astuple(
    obj: Mapping[str, Any],
    /,
    *,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of a mapping as a tuple.

    Examples
    --------
    >>> from dataclassish import astuple

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> astuple(p)
    (1, 2.0, '3')

    """
    return tuple_factory(obj.values())
