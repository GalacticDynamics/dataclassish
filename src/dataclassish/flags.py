"""flags for ``dataclassish``."""

__all__ = ["FlagConstructionError", "AbstractFlag", "NoFlag", "FilterRepr"]

from ._src.flag_compat import *  # noqa: F403
from ._src.flags import AbstractFlag, FilterRepr, FlagConstructionError, NoFlag
