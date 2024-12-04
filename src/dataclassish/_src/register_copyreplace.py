"""Register dispatches for CanCopyReplace objects."""

__all__: list[str] = []

import copy
import sys
from collections.abc import Mapping
from typing import Any

from plum import dispatch

from .register_base import _recursive_replace_helper
from .types import CanCopyReplace

# ===================================================================
# Get field


@dispatch  # type: ignore[misc]
def get_field(obj: CanCopyReplace, k: str, /) -> Any:
    """Get a field of a dataclass instance by name.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import get_field

    % invisible-code-block: python
    %
    % import sys

    % skip: start if(sys.version_info < (3, 13), reason="py3.13+")

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> get_field(p, "x")
    1.0

    % skip: end

    This works for any object that implements the ``__replace__`` method.

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...     def __replace__(self, **changes):
    ...         return Point(**(self.__dict__ | changes))
    ...     def __repr__(self):
    ...         return f"Point(x={self.x}, y={self.y})"

    >>> p = Point(1.0, 2.0)
    >>> get_field(p, "x")
    1.0

    """
    return getattr(obj, k)


# ===================================================================
# Replace


@dispatch
def replace(obj: CanCopyReplace, /, **kwargs: Any) -> CanCopyReplace:
    """Replace the fields of an object.

    Examples
    --------
    >>> from dataclassish import replace

    % invisible-code-block: python
    %
    % import sys

    % skip: start if(sys.version_info < (3, 13), reason="py3.13+")

    As of Python 3.13, dataclasses implement the ``__replace__`` method.

    >>> from dataclasses import dataclass

    >>> @dataclass
    ... class Point:
    ...     x: float
    ...     y: float

    >>> p = Point(1.0, 2.0)
    >>> p
    Point(x=1.0, y=2.0)

    >>> replace(p, x=3.0)
    Point(x=3.0, y=2.0)

    % skip: end

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...     def __replace__(self, **changes):
    ...         return Point(**(self.__dict__ | changes))
    ...     def __repr__(self):
    ...         return f"Point(x={self.x}, y={self.y})"

    >>> p = Point(1.0, 2.0)
    >>> replace(p, x=2.0)
    Point(x=2.0, y=2.0)

    The ``__replace__`` method was introduced in Python 3.13 to bring
    ``dataclasses.replace``-like functionality to any implementing object. The
    method is publicly exposed via the ``copy.replace`` function.

    % invisible-code-block: python
    %
    % import sys

    % skip: start if(sys.version_info < (3, 13), reason="py3.13+")

    >>> import copy
    >>> copy.replace(p, x=3.0)
    Point(x=3.0, y=2.0)

    % skip: end

    """
    return (
        obj.__replace__(**kwargs)
        if sys.version_info < (3, 13)
        else copy.replace(obj, **kwargs)
    )


@dispatch  # type: ignore[no-redef]
def replace(obj: CanCopyReplace, fs: Mapping[str, Any], /) -> CanCopyReplace:
    """Replace the fields of a dataclass instance.

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> from dataclassish import replace, F

    >>> class Point:
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    ...     def __replace__(self, **changes):
    ...         return Point(**(self.__dict__ | changes))
    ...     def __repr__(self):
    ...         return f"Point(x={self.x}, y={self.y})"

    >>> @dataclass
    ... class TwoPoint:
    ...     a: Point
    ...     b: Point

    >>> p = TwoPoint(Point(1.0, 2.0), Point(3.0, 4.0))
    >>> p
    TwoPoint(a=Point(x=1.0, y=2.0), b=Point(x=3.0, y=4.0))

    >>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
    TwoPoint(a=Point(x=5.0, y=2.0), b=Point(x=3.0, y=6.0))

    >>> replace(p, {"a": {"x": F({"thing": 5.0})}})
    TwoPoint(a=Point(x={'thing': 5.0}, y=2.0),
                b=Point(x=3.0, y=4.0))

    This also works on mixed-type structures, e.g. a dictionary of objects.

    >>> p = {"a": Point(1.0, 2.0), "b": Point(3.0, 4.0)}
    >>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
    {'a': Point(x=5.0, y=2.0), 'b': Point(x=3.0, y=6.0)}

    """
    kwargs = {k: _recursive_replace_helper(obj, k, v) for k, v in fs.items()}
    return replace(obj, **kwargs)
