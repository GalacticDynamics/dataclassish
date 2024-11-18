"""Converters for dataclass fields.

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: ``attrs`` and ``equinox``. This module provides a few useful converter
functions. If you need more, check out ``attrs``!

"""

__all__ = ["AbstractConverter", "Optional", "Unless"]

from ._src.converters import AbstractConverter, Optional, Unless
