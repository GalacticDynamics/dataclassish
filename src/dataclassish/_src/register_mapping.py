"""Register dispatches for mapping objects."""

__all__: list[str] = []

from collections.abc import Callable, Hashable, ItemsView, KeysView, Mapping, ValuesView
from dataclasses import Field, field
from typing import Any

from plum import dispatch

from .types import F

# ===================================================================


@dispatch(precedence=1)  # type: ignore[misc]
def get_field(obj: Mapping[Hashable, Any], k: Hashable, /) -> Any:
    """Get a field of a mapping by key.

    Examples
    --------
    >>> from dataclassish import get_field

    >>> p = {"a": 1, "b": 2.0, "c": "3"}
    >>> get_field(p, "a")
    1

    """
    return obj[k]


# ===================================================================
# Replace


@dispatch  # type: ignore[misc]
def replace(obj: Mapping[str, Any], /, **kwargs: Any) -> Mapping[str, Any]:
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

    Extra keys are not allowed:

    >>> try: replace(p, d=5)
    ... except ValueError as e: print(e)
    invalid keys {'d'}.

    """
    extra_keys = set(kwargs) - set(obj)
    if extra_keys:
        msg = f"invalid keys {extra_keys}."
        raise ValueError(msg)

    return type(obj)(**{**obj, **kwargs})


def _recursive_replace_mapping_helper(
    obj: Mapping[Hashable, Any], k: str, v: Any, /
) -> Any:
    if isinstance(v, F):  # Field, stop here.
        out = v.value
    elif isinstance(v, Mapping):  # more to replace, recurse.
        out = replace(get_field(obj, k), v)
    else:  # nothing to replace, keep the value.
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

    This also works on mixed-type structures, e.g. a dataclass of of dictionaries.

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Object:
    ...     a: dict[str, Any]
    ...     b: dict[str, Any]

    >>> p = Object({"a": 1, "b": 2}, {"c": 3, "d": 4})
    >>> replace(p, {"a": {"b": 5}, "b": {"c": 6}})
    Object(a={'a': 1, 'b': 5}, b={'c': 6, 'd': 4})

    """
    # Recursively replace the fields
    kwargs = {k: _recursive_replace_mapping_helper(obj, k, v) for k, v in fs.items()}

    return type(obj)(**(dict(obj) | kwargs))


# ===================================================================
# Fields


@dispatch  # type: ignore[misc]
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


@dispatch  # type: ignore[misc]
def asdict(
    obj: Mapping[Hashable, Any],
    /,
    *,
    dict_factory: Callable[[Mapping[Hashable, Any]], dict[Hashable, Any]] = dict,
) -> dict[Hashable, Any]:
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


@dispatch  # type: ignore[misc]
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


# ===================================================================
# Field keys


@dispatch  # type: ignore[misc]
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


@dispatch  # type: ignore[misc]
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


@dispatch  # type: ignore[misc]
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
