"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

dataclassish: dataclass tools, extended by multiple dispatch
"""

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

from . import converters, flags
from ._src.api import (
    asdict,
    astuple,
    field_items,
    field_keys,
    field_values,
    fields,
    replace,
)
from ._src.types import DataclassInstance, F
from ._version import version as __version__

# Register dispatches by importing the submodules
# isort: split
from ._src import register_base, register_dataclass, register_mapping

del register_base, register_dataclass, register_mapping
