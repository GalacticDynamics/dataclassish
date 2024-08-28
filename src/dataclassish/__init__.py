"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

dataclassish: dataclass tools, extended by multiple dispatch
"""

from . import converters
from ._core import DataclassInstance, F, asdict, astuple, fields, replace
from ._ext import field_items, field_keys, field_values
from ._version import version as __version__

__all__ = [
    "__version__",
    "converters",
    # core
    "DataclassInstance",
    "replace",
    "fields",
    "asdict",
    "astuple",
    # ext
    "field_keys",
    "field_values",
    "field_items",
    "F",
]
