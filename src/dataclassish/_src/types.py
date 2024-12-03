"""Data types for ``dataclassish``."""

__all__ = ["DataclassInstance", "F"]

from dataclasses import dataclass
from typing import Any, ClassVar, Generic, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class DataclassInstance(Protocol):
    """Protocol for dataclass instances.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import DataclassInstance

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> issubclass(Point, DataclassInstance)
    True

    >>> point = Point(1.0, 2.0)

    >>> isinstance(point, DataclassInstance)
    True

    """

    __dataclass_fields__: ClassVar[dict[str, Any]]

    # B/c of https://github.com/python/mypy/issues/3939 just having
    # `__dataclass_fields__` is insufficient for `issubclass` checks.
    @classmethod
    def __subclasshook__(cls: type, c: type) -> bool:
        """Customize the subclass check."""
        return hasattr(c, "__dataclass_fields__")


# ===================================================================

V = TypeVar("V")


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
