"""flags for ``dataclassish``."""

__all__ = ["FlagConstructionError", "AbstractFlag"]

from typing import Any


class FlagConstructionError(Exception):
    """Flag construction error."""

    def __init__(self, flag_type: str) -> None:
        super().__init__(f"{flag_type} flag cannot be constructed.")


class AbstractFlag:
    """Abstract class for flags to provide dispatch control.

    Flags are not intended to be instantiated and are used to provide dispatch
    controls.

    Raises
    ------
    FlagConstructionError
        If an attempt is made to instantiate a unit system flag class.

    Examples
    --------
    >>> from dataclassish.flags import AbstractFlag
    >>> try: AbstractFlag()
    ... except FlagConstructionError as e: print(e)
    AbstractFlag flag cannot be constructed.

    """

    def __new__(cls, *_: Any, **__: Any) -> None:  # type: ignore[misc]
        raise FlagConstructionError(cls.__name__)


class NoFlag(AbstractFlag):
    """No flag."""
