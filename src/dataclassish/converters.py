"""Converters for dataclass fields.

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: ``attrs`` and ``equinox``. This module provides a few useful converter
functions. If you need more, check out ``attrs``!

This library also provide a lightweight dataclass-like decorator and field
function that supports these converters and converters in general.

>>> from dataclassish.converters import dataclass, field, Optional

>>> @dataclass
... class MyClass:
...     a: int | None = field(converter=Optional(int))
...     b: str = field(converter=str.upper)

>>> obj = MyClass(a="1", b="hello")
>>> obj
MyClass(a=1, b='HELLO')

>>> obj = MyClass(a=None, b="there")
>>> obj
MyClass(a=None, b='THERE')

"""

__all__ = ["AbstractConverter", "Optional", "Unless", "field", "dataclass"]

from ._src.converters import AbstractConverter, Optional, Unless, dataclass, field
