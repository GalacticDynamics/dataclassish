"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

dataclassish: dataclass tools, extended by multiple dispatch
"""

from . import converters, flags
from ._src.core import F, asdict, astuple, fields, replace
from ._src.ext import field_items, field_keys, field_values
from ._src.types import DataclassInstance
from ._version import version as __version__

__all__ = [
    "__version__",
    # Submodules
    "converters",
    "flags",
    # Dataclass API
    "DataclassInstance",
    "replace",
    "fields",
    "asdict",
    "astuple",
    # Extensions
    "field_keys",
    "field_values",
    "field_items",
    "F",
]
