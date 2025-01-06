"""Data types for ``dataclassish``."""

__all__ = ["DataclassInstance", "CanCopyReplace", "F"]

from dataclasses import dataclass
from typing import Any, ClassVar, Generic, Protocol, TypeVar, runtime_checkable
from typing_extensions import Self


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


# ===================================================================


@runtime_checkable
class CanCopyReplace(Protocol):
    """Protocol for objects that implement the ``__replace__`` method.

    This is used by ``copy.replace`` (Python 3.13+) to replace fields of an
    object.  This is a generalization of the ``dataclasses.replace`` function.

    Examples
    --------
    >>> from dataclassish import CanCopyReplace

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...     def __replace__(self, **changes):
    ...         return Point(**(self.__dict__ | changes))
    ...     def __repr__(self):
    ...         return f"Point(x={self.x}, y={self.y})"

    >>> issubclass(Point, CanCopyReplace)
    True

    >>> point = Point(1.0, 2.0)
    >>> isinstance(point, CanCopyReplace)
    True

    The ``__replace__`` method was introduced in Python 3.13 to bring
    ``dataclasses.replace``-like functionality to any implementing object. The
    method is publicly exposed via the ``copy.replace`` function.

    % invisible-code-block: python
    %
    % import sys

    % skip: start if(sys.version_info < (3, 13), reason="py3.13+")

    >>> import copy
    >>> copy.replace(point, x=3.0)
    Point(x=3.0, y=2.0)

    % skip: end

    """

    def __replace__(self: Self, /, **changes: Any) -> Self:
        """Replace the fields of the object.

        This method should return a new object with the fields replaced.

        """
