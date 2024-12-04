"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

dataclassish: dataclass tools, extended by multiple dispatch
"""

__all__ = [
    "__version__",
    # Submodules
    "converters",
    "flags",
    # functions
    "replace",
    "fields",
    "asdict",
    "astuple",
    "get_field",
    "field_keys",
    "field_values",
    "field_items",
    # Classes
    "DataclassInstance",
    "F",
]

from . import converters, flags
from ._src.api import (
    asdict,
    astuple,
    field_items,
    field_keys,
    field_values,
    fields,
    get_field,
    replace,
)
from ._src.types import DataclassInstance, F
from ._version import version as __version__

# Register dispatches by importing the submodules
# isort: split
from ._src import register_base, register_dataclass, register_mapping

del register_base, register_dataclass, register_mapping
