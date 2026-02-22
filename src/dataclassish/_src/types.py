"""Data types for ``dataclassish``."""

__all__ = ("F",)

from dataclasses import dataclass
from typing import Generic, TypeVar

V = TypeVar("V")


@dataclass(frozen=True, slots=True)
class F(Generic[V]):
    """Mark a field as a dataclass field when doing multi-level replacement.

    Examples
    --------
    >>> from dataclassish import F, replace

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
