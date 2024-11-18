"""flags for ``dataclassish``."""

__all__ = ["FlagConstructionError", "AbstractFlag", "NoFlag"]

from ._src.flag_compat import *  # noqa: F403
from ._src.flags import AbstractFlag, FlagConstructionError, NoFlag
