"""flags for ``dataclassish``."""

__all__: list[str] = []

from collections.abc import Callable, Iterable
from dataclasses import Field
from typing import Any, cast

from plum import dispatch
from typing_extensions import Never

from .flags import AbstractFlag, NoFlag

# ===================================================================
# AbstractFlag


@dispatch  # type: ignore[misc]
def replace(flag: type[AbstractFlag], _: Any, /, **__: Any) -> Never:  # noqa: ARG001
    """Raise an error if given an AbstractFlag when replacing.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import replace
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: replace(AbstractFlag, p, x=3.0)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def fields(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used to get fields.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import fields
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: fields(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def asdict(
    flag: type[AbstractFlag],  # noqa: ARG001
    _: Any,
    /,
    *,
    dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict,  # noqa: ARG001
) -> Never:
    """Raise an error if an AbstractFlag is used with ``asdict``.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import asdict
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: asdict(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def astuple(
    flag: type[AbstractFlag],  # noqa: ARG001
    _: Any,
    /,
    *,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,  # noqa: ARG001
) -> Never:
    """Raise an error if an AbstractFlag is used with ``asdict``.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import astuple
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: astuple(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def field_keys(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_keys``.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import field_keys
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: field_keys(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def field_values(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_values``.

    Raises
    ------
    ValueError

    Examples
    --------
    >>> from dataclassish import field_values
    >>> from dataclassish.flags import AbstractFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> try: field_values(AbstractFlag, p)
    ... except ValueError as e: print(e)
    Do not use the AbstractFlag directly, only use subclasses.

    """
    msg = "Do not use the AbstractFlag directly, only use subclasses."
    raise ValueError(msg)


@dispatch  # type: ignore[misc]
def field_items(flag: type[AbstractFlag], _: Any, /) -> Never:  # noqa: ARG001
    """Raise an error if an AbstractFlag is used with ``field_items``.

    Raises
    ------
    ValueError

    Examples
    --------
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


@dispatch  # type: ignore[misc, no-redef]
def replace(flag: type[NoFlag], obj: Any, /, **kwargs: Any) -> Any:  # noqa: ARG001
    """Replace the fields of an object, absent any modifying flags.

    Examples
    --------
    >>> from dataclassish import replace
    >>> from dataclassish.flags import NoFlag

    >>> p = {"x": 1.0, "y": 2.0}

    >>> replace(NoFlag, p, x=3.0)
    {'x': 3.0, 'y': 2.0}

    """
    return replace(obj, **kwargs)


@dispatch  # type: ignore[misc, no-redef]
def fields(flag: type[NoFlag], obj: Any, /) -> tuple[Field, ...]:  # type: ignore[type-arg]  # noqa: ARG001
    """Return fields of the object, absent any modifying flags.

    Examples
    --------
    >>> from dataclassish import fields
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> fields(NoFlag, p)
    (Field(name='a',type=<class 'int'>,...),
     Field(name='b',type=<class 'float'>,...),
     Field(name='c',type=<class 'str'>,...))

    """
    return cast(tuple[Field, ...], fields(obj))  # type: ignore[type-arg]


@dispatch  # type: ignore[misc, no-redef]
def asdict(
    flag: type[NoFlag],  # noqa: ARG001
    obj: Any,
    /,
    *,
    dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict,
) -> dict[str, Any]:
    """Return the fields as a mapping, absent any modifying flags.

    Examples
    --------
    >>> from dataclassish import asdict
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> asdict(NoFlag, p)
    {'a': 1, 'b': 2.0, 'c': '3'}

    >>> asdict(p) is p
    False

    """
    return cast(dict[str, Any], asdict(obj, dict_factory=dict_factory))


@dispatch  # type: ignore[misc, no-redef]
def astuple(
    flag: type[NoFlag],  # noqa: ARG001
    obj: Any,
    /,
    *,
    tuple_factory: Callable[[Any], tuple[Any, ...]] = tuple,
) -> tuple[Any, ...]:
    """Return the fields of an object as a tuple, absent any modifying flags.

    Examples
    --------
    >>> from dataclassish import astuple
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> astuple(NoFlag, p)
    (1, 2.0, '3')

    """
    return cast(tuple[Any, ...], astuple(obj, tuple_factory=tuple_factory))


@dispatch  # type: ignore[misc, no-redef]
def field_keys(flag: type[NoFlag], obj: Any, /) -> Iterable[Any]:  # noqa: ARG001
    """Return the keys of an object.

    Examples
    --------
    >>> from dataclassish import field_keys
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_keys(NoFlag, p)
    dict_keys(['a', 'b', 'c'])

    """
    return cast(Iterable[Any], field_keys(obj))


@dispatch  # type: ignore[misc, no-redef]
def field_values(flag: type[NoFlag], obj: Any, /) -> Iterable[Any]:  # noqa: ARG001
    """Return the values of an object.

    Examples
    --------
    >>> from dataclassish import field_values
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_values(NoFlag, p)
    dict_values([1, 2.0, '3'])

    """
    return cast(Iterable[Any], field_values(obj))


@dispatch  # type: ignore[misc, no-redef]
def field_items(flag: type[NoFlag], obj: Any, /) -> Iterable[tuple[Any, Any]]:  # noqa: ARG001
    """Return the items of an object.

    Examples
    --------
    >>> from dataclassish import field_items
    >>> from dataclassish.flags import NoFlag

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> field_items(NoFlag, p)
    dict_items([('a', 1), ('b', 2.0), ('c', '3')])

    """
    return cast(Iterable[tuple[Any, Any]], field_items(obj))
