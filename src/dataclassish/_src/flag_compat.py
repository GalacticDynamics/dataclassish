"""flags for ``dataclassish``."""

__all__: tuple[str, ...] = ()

from collections.abc import Iterable
from dataclasses import Field
from typing import Any, Never, cast

from plum import dispatch

from . import api
from .flags import AbstractFlag, FilterRepr, NoFlag

# ===================================================================
# AbstractFlag


@dispatch
def replace(flag: type[AbstractFlag], _: Any, /, **__: Any) -> Never:  # noqa: ARG001
    """Raise an error if given an AbstractFlag when replacing.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import replace
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: replace(AbstractFlag, p, x=3.0)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def fields(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used to get fields.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import fields
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: fields(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def asdict(
    flag: type[AbstractFlag],  # noqa: ARG001
    _: Any,
    /,
    *,
    dict_factory: api.DictFactory = dict,  # noqa: ARG001
) -> Never:
    """Raise an error if an AbstractFlag is used with ``asdict``.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import asdict
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: asdict(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def astuple(
    flag: type[AbstractFlag],  # noqa: ARG001
    _: Any,
    /,
    *,
    tuple_factory: api.TupleFactory = tuple,  # noqa: ARG001
) -> Never:
    """Raise an error if an AbstractFlag is used with ``asdict``.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import astuple
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: astuple(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def field_keys(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_keys``.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import field_keys
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: field_keys(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def field_values(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_values``.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import field_values
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: field_values(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch
def field_items(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_items``.

    Raises:
        ValueError

    Examples:
    >>> from dataclassish import field_items
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: field_items(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


# ===================================================================
# NoFlag


@dispatch  # type: ignore[no-redef]
def replace(flag: type[NoFlag], obj: Any, /, **kwargs: Any) -> Any:  # noqa: ARG001
    """Replace the fields of an object, absent any modifying flags.

    Examples:
    >>> from dataclassish import replace
    >>> from dataclassish.flags import NoFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> replace(NoFlag, p, x=3.0)
    {'x': 3.0, 'y': 2.0}

    """
    return api.replace(obj, **kwargs)


@dispatch  # type: ignore[no-redef]
def fields(flag: type[NoFlag], obj: Any, /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # noqa: ARG001
    """Return fields of the object, absent any modifying flags.

    Examples:
    >>> from dataclassish import fields
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> fields(NoFlag, p)
    (Field(name='a',type=<class 'int'>,...),
     Field(name='b',type=<class 'float'>,...),
     Field(name='c',type=<class 'str'>,...))

    """
    return cast("tuple[Field, ...]", api.fields(obj))  # type: ignore[type-arg]


@dispatch  # type: ignore[no-redef]
def asdict(
    flag: type[NoFlag],  # noqa: ARG001
    obj: Any,
    /,
    *,
    dict_factory: api.DictFactory = dict,
) -> dict[str, Any]:
    """Return the fields as a mapping, absent any modifying flags.

    Examples:
    >>> from dataclassish import asdict
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> asdict(NoFlag, p)
    {'a': 1, 'b': 2.0, 'c': '3'}

    >>> asdict(p) is p
    False

    """
    return cast("dict[str, Any]", api.asdict(obj, dict_factory=dict_factory))


@dispatch  # type: ignore[no-redef]
def astuple(
    flag: type[NoFlag],  # noqa: ARG001
    obj: Any,
    /,
    *,
    tuple_factory: api.TupleFactory = tuple,
) -> tuple[Any, ...]:
    """Return the fields of an object as a tuple, absent any modifying flags.

    Examples:
    >>> from dataclassish import astuple
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> astuple(NoFlag, p)
    (1, 2.0, '3')

    """
    return cast("tuple[Any, ...]", api.astuple(obj, tuple_factory=tuple_factory))


@dispatch  # type: ignore[no-redef]
def field_keys(flag: type[NoFlag], obj: Any, /) -> Iterable[Any]:  # noqa: ARG001
    """Return the keys of an object.

    Examples:
    >>> from dataclassish import field_keys
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_keys(NoFlag, p)
    dict_keys(['a', 'b', 'c'])

    """
    return cast("Iterable[Any]", api.field_keys(obj))


@dispatch  # type: ignore[no-redef]
def field_values(flag: type[NoFlag], obj: Any, /) -> Iterable[Any]:  # noqa: ARG001
    """Return the values of an object.

    Examples:
    >>> from dataclassish import field_values
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_values(NoFlag, p)
    dict_values([1, 2.0, '3'])

    """
    return cast("Iterable[Any]", api.field_values(obj))


@dispatch  # type: ignore[no-redef]
def field_items(flag: type[NoFlag], obj: Any, /) -> Iterable[tuple[Any, Any]]:  # noqa: ARG001
    """Return the items of an object.

    Examples:
    >>> from dataclassish import field_items
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_items(NoFlag, p)
    dict_items([('a', 1), ('b', 2.0), ('c', '3')])

    """
    return cast("Iterable[tuple[Any, Any]]", api.field_items(obj))


# ===================================================================
# FilterRepr


@dispatch  # type: ignore[no-redef]
def replace(_: type[FilterRepr], obj: Any, /, **kwargs: Any) -> Any:
    """Replace the fields of an object, filtering based on repr.

    Raises:
        ValueError: If a field is in kwargs but has repr=False.

    Examples:
    >>> from dataclassish import replace
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> replace(FilterRepr, obj, x=3.0)
    Point(x=3.0)

    >>> try: replace(FilterRepr, obj, y=3.0)
    ... except ValueError as e: print(e)
    Fields ['y'] are in kwargs but are repr=False.

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> replace(FilterRepr, obj, x=3.0)
    {'x': 3.0, 'y': 2.0}

    """
    # Determine if any changes are
    fs_in_kw_but_repr = [
        f.name for f in api.fields(obj) if f.name in kwargs if not f.repr
    ]
    if fs_in_kw_but_repr:
        msg = f"Fields {fs_in_kw_but_repr} are in kwargs but are repr=False."
        raise ValueError(msg)

    return api.replace(obj, **kwargs)


@dispatch  # type: ignore[no-redef]
def fields(_: type[FilterRepr], obj: Any) -> tuple[Field, ...]:  # type: ignore[type-arg]
    """Return fields of the object, filtering based on repr.

    Examples:
    >>> from dataclassish import fields
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> fields(FilterRepr, obj)
    (Field(name='x',...),)

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> fields(FilterRepr, obj)
    (Field(name='x',...), Field(name='y',...))

    """
    return tuple(f for f in api.fields(obj) if f.repr)


@dispatch  # type: ignore[no-redef]
def asdict(
    flag: type[FilterRepr], obj: Any, /, *, dict_factory: api.DictFactory = dict
) -> dict[str, Any]:
    """Return the fields as a mapping, filtering based on repr.

    Examples:
    >>> from dataclassish import asdict
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> asdict(FilterRepr, obj)
    {'x': 1.0}

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> asdict(FilterRepr, obj)
    {'x': 1.0, 'y': 2.0}

    """
    all_dict = api.asdict(obj)
    keep_keys = api.field_keys(flag, obj)
    return dict_factory([(k, all_dict[k]) for k in keep_keys])


@dispatch  # type: ignore[no-redef]
def astuple(
    _: type[FilterRepr],
    obj: Any,
    /,
    *,
    tuple_factory: api.TupleFactory = tuple,
) -> tuple[Any, ...]:
    """Return the fields of an object as a tuple, filtering based on repr.

    Examples:
    >>> from dataclassish import astuple
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> astuple(FilterRepr, obj)
    (1.0,)

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> astuple(FilterRepr, obj)
    (1.0, 2.0)

    """
    tup = api.astuple(obj)
    keep = [f.repr for f in api.fields(obj)]
    return tuple_factory([x for x, cond in zip(tup, keep, strict=True) if cond])


@dispatch
def get_field(_: type[FilterRepr], obj: Any, field_name: str) -> Any:
    """Get the value of a field from an object, filtering based on repr.

    Raises:
        ValueError: If the field is repr=False.

    Examples:
    >>> from dataclassish import get_field
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> get_field(FilterRepr, obj, "x")
    1.0

    >>> try: get_field(FilterRepr, obj, "z")
    ... except ValueError as e: print(e)
    Field z not found.

    >>> try: get_field(FilterRepr, obj, "y")
    ... except ValueError as e: print(e)
    Field y is repr=False.

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> get_field(FilterRepr, obj, "x")
    1.0

    """
    f = [f.repr for f in api.fields(obj) if f.name == field_name]
    if not f:
        msg = f"Field {field_name} not found."
        raise ValueError(msg)
    if not f[0]:
        msg = f"Field {field_name} is repr=False."
        raise ValueError(msg)

    return api.get_field(obj, field_name)


@dispatch  # type: ignore[no-redef]
def field_keys(_: type[FilterRepr], obj: Any) -> tuple[Any, ...]:
    """Return the keys of an object, filtering based on repr.

    Examples:
    >>> from dataclassish import field_keys
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> field_keys(FilterRepr, obj)
    ('x',)

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> field_keys(FilterRepr, obj)
    ('x', 'y')

    """
    return tuple(
        k for k, f in zip(api.field_keys(obj), api.fields(obj), strict=True) if f.repr
    )


@dispatch  # type: ignore[no-redef]
def field_values(_: type[FilterRepr], obj: Any) -> tuple[Any, ...]:
    """Return the values of an object, filtering based on repr.

    Examples:
    >>> from dataclassish import field_values
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> field_values(FilterRepr, obj)
    (1.0,)

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> field_values(FilterRepr, obj)
    (1.0, 2.0)

    """
    return tuple(
        v for v, f in zip(api.field_values(obj), api.fields(obj), strict=True) if f.repr
    )


@dispatch  # type: ignore[no-redef]
def field_items(_: type[FilterRepr], obj: Any) -> tuple[tuple[Any, Any], ...]:
    """Return the items of an object, filtering based on repr.

    Examples:
    >>> from dataclassish import field_items
    >>> from dataclassish.flags import FilterRepr

    1) dataclass:

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float = field(repr=False)
    >>> obj = Point(1.0, 2.0)

    >>> field_items(FilterRepr, obj)
    (('x', 1.0),)

    2) dict:

    >>> obj = {"x": 1.0, "y": 2.0}
    >>> field_items(FilterRepr, obj)
    (('x', 1.0), ('y', 2.0))

    """
    return tuple(
        (k, v)
        for (k, v), f in zip(api.field_items(obj), api.fields(obj), strict=True)
        if f.repr
    )
