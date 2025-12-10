"""flags for ``dataclassish``."""

__all__ = ("FlagConstructionError", "AbstractFlag", "NoFlag", "FilterRepr")

from ._src.flags import AbstractFlag, FilterRepr, FlagConstructionError, NoFlag

# Need to import to register the dispatches
# isort: split
from ._src.flag_compat import *  # noqa: F403  # pylint: disable=wildcard-import,unused-wildcard-import
