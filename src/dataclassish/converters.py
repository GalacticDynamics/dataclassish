"""Converters for dataclass fields.

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: ``attrs`` and ``equinox``. This module provides a few useful converter
functions. If you need more, check out ``attrs``!

A quick rant of why rejecting PEP 712 was a bad idea. A core design guideline
for Python is Postel's Law: "be conservative in what you send, be liberal in
what you accept" (https://en.wikipedia.org/wiki/Robustness_principle). Currently
dataclasses are conservative in what they "send" (i.e., the types of their
attributes when accessed from an instance of a dataclass). The problem is that
without converters dataclasses are ALSO conservative in what they "accept" (how
they can be initialized), since they require that the types of the attributes
match the types of the fields. The onus of data structuring is forced on the
user. This is a violation of Postel's Law. Without PEP 712's converter support
the only way to be liberal in the what dataclasses accept is to write a custom
``__init__`` method, in which case why are we even using a dataclass?! The
rejection of PEP 712 directly contradicts a core design principle of Python.

"""
# ruff:noqa: N801
# pylint: disable=C0103

__all__ = ["AbstractConverter", "Optional", "Unless"]

import dataclasses
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any, Generic, TypeVar, cast, overload

ArgT = TypeVar("ArgT")  # Input type
RetT = TypeVar("RetT")  # Return type


class AbstractConverter(Generic[ArgT, RetT], metaclass=ABCMeta):
    """Abstract converter class."""

    converter: Callable[[ArgT], RetT]
    """The converter to apply to the input value."""

    @abstractmethod
    def __call__(self, value: ArgT, /) -> Any:
        """Convert the input value to the desired output type."""
        raise NotImplementedError  # pragma: no cover


# -------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Optional(AbstractConverter[ArgT, RetT]):
    """Optional converter with a defined sentinel value.

    This converter allows for a field to be optional, i.e., it can be set to
    `None`.  This is useful when a field is required in some contexts but not in
    others.

    This converter is based on ``attr.converters.optional``. If ``attrs`` ever
    separates this out into its own package, so that other libraries, like
    ``equinox``, can use the converter without depending on ``attrs``, then this
    implementation will probably be removed.

    Examples
    --------
    For this example we will use ``attrs`` as the dataclass library, but this
    converter can be used with any dataclass-like library that supports
    converters.

    >>> from attrs import define, field
    >>> from dataclassish.converters import Optional

    >>> @define
    ... class Class:
    ...     attr: int | None = field(default=None, converter=Optional(int))

    >>> obj = Class()
    >>> print(obj.attr)
    None

    >>> obj = Class(1)
    >>> obj.attr
    1

    """

    converter: Callable[[ArgT], RetT]
    """The converter to apply to the input value."""

    @overload
    def __call__(self, value: None, /) -> None: ...

    @overload
    def __call__(self, value: ArgT, /) -> RetT: ...

    def __call__(self, value: ArgT | None, /) -> RetT | None:
        """Convert the input value to the output type, passing through `None`."""
        return None if value is None else self.converter(value)


# -------------------------------------------------------------------

PassThroughTs = TypeVar("PassThroughTs")


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Unless(AbstractConverter[ArgT, RetT], Generic[ArgT, PassThroughTs, RetT]):
    """Converter that is applied if the argument is NOT a specified type.

    This converter is useful when you want to pass through a value if it is of a
    certain type, but convert it otherwise.

    Examples
    --------
    For this example we will use ``attrs`` as the dataclass library, but this
    converter can be used with any dataclass-like library that supports
    converters.

    >>> from attrs import define, field
    >>> from dataclassish.converters import Unless

    >>> @define
    ... class Class:
    ...     attr: float | int = field(converter=Unless(int, converter=float))

    >>> obj = Class(1)
    >>> obj.attr
    1

    >>> obj = Class("1")
    >>> obj.attr
    1.0

    """

    unconverted_types: type[PassThroughTs] | tuple[type[PassThroughTs], ...]
    """The types to pass through without conversion."""

    converter: Callable[[ArgT], RetT]
    """The converter to apply to the input value."""

    @overload
    def __call__(self, value: ArgT, /) -> RetT: ...

    @overload
    def __call__(self, value: PassThroughTs, /) -> PassThroughTs: ...

    def __call__(self, value: ArgT | PassThroughTs, /) -> RetT | PassThroughTs:
        """Pass through the input value."""
        return (
            cast(PassThroughTs, value)
            if isinstance(value, self.unconverted_types)
            else self.converter(cast(ArgT, value))
        )
