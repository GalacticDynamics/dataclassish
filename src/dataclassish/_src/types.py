"""Data types for ``dataclassish``."""

__all__ = [
    "DataclassInstance",
]

from typing import Any, ClassVar, Protocol, runtime_checkable


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
