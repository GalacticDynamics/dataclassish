"""Converters for dataclass fields.

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: ``attrs`` and ``equinox``. This module provides a few useful converter
functions. If you need more, check out ``attrs``!

"""
# ruff:noqa: N801
# pylint: disable=C0103

__all__ = [
    # Converters
    "AbstractConverter",
    "Optional",
    "Unless",
    # Minimal dataclass implementation
    "dataclass",
    "field",
]

import dataclasses
import functools
import inspect
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Hashable, Mapping
from typing import (
    Any,
    ClassVar,
    Generic,
    Protocol,
    TypeVar,
    cast,
    overload,
)
from typing_extensions import dataclass_transform

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


#####################################################################
# Minimal implementation of a dataclass supporting converters.

_CT = TypeVar("_CT")


def field(
    *,
    converter: Callable[[Any], Any] | None = None,
    metadata: Mapping[Hashable, Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Dataclass field with a converter argument.

    Parameters
    ----------
    converter : callable, optional
        A callable that converts the value of the field. This is added to the
        metadata of the field.
    metadata : Mapping[Hashable, Any], optional
        Additional metadata to add to the field.
        See `dataclasses.field` for more information.
    **kwargs : Any
        Additional keyword arguments to pass to `dataclasses.field`.

    """
    if converter is not None:
        # Check the converter
        if not callable(converter):
            msg = f"converter must be callable, got {converter!r}"  # type: ignore[unreachable]
            raise TypeError(msg)

        # Convert the metadata to a mutable dict if it is not None.
        metadata = dict(metadata) if metadata is not None else {}

        if "converter" in metadata:
            msg = "cannot specify 'converter' in metadata and as a keyword argument."
            raise ValueError(msg)

        # Add the converter to the metadata
        metadata["converter"] = converter

    return dataclasses.field(metadata=metadata, **kwargs)


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]


def _process_dataclass(cls: type[_CT], **kwargs: Any) -> type[_CT]:
    # Make the dataclass from the class.
    # This does all the usual dataclass stuff.
    dcls: type[_CT] = dataclasses.dataclass(cls, **kwargs)

    # Compute the signature of the __init__ method
    sig = inspect.signature(dcls.__init__)
    # Eliminate the 'self' parameter
    sig = sig.replace(parameters=list(sig.parameters.values())[1:])
    # Store the signature on the __init__ method (Not assigning to __signature__
    # because that should have `self`).
    dcls.__init__._obj_signature_ = sig  # type: ignore[attr-defined]

    # Ensure that the __init__ method does conversion
    @functools.wraps(dcls.__init__)  # give it the same signature
    def init(
        self: DataclassInstance, *args: Any, _skip_convert: bool = False, **kwargs: Any
    ) -> None:
        # Fast path: no conversion
        if _skip_convert:
            self.__init__.__wrapped__(self, *args, **kwargs)  # type: ignore[misc]
            return

        # Bind the arguments to the signature
        ba = self.__init__._obj_signature_.bind_partial(*args, **kwargs)  # type: ignore[misc]
        ba.apply_defaults()  # so eligible for conversion

        # Convert the fields, if there's a converter
        for f in dataclasses.fields(self):
            k = f.name
            if k not in ba.arguments:  # mandatory field not provided?!
                continue  # defer the error to the dataclass __init__

            converter = f.metadata.get("converter")
            if converter is not None:
                ba.arguments[k] = converter(ba.arguments[k])

        #  Call the original dataclass __init__ method
        self.__init__.__wrapped__(self, *ba.args, **ba.kwargs)  # type: ignore[misc]

    dcls.__init__ = init  # type: ignore[assignment, method-assign]

    return dcls


@overload
def dataclass(cls: type[_CT], /, **kwargs: Any) -> type[_CT]: ...


@overload
def dataclass(**kwargs: Any) -> Callable[[type[_CT]], type[_CT]]: ...


@dataclass_transform(field_specifiers=(dataclasses.Field, dataclasses.field, field))
def dataclass(
    cls: type[_CT] | None = None, /, **kwargs: Any
) -> type[_CT] | Callable[[type[_CT]], type[_CT]]:
    """Make a dataclass, supporting field converters.

    For more information about dataclasses see the `dataclasses` module.

    Parameters
    ----------
    cls : type | None, optional
        The class to transform into a dataclass. If `None`, returns a partial
        function that can be used as a decorator.
    **kwargs : Any
        Additional keyword arguments to pass to `dataclasses.dataclass`.

    Examples
    --------
    >>> from dataclassish.converters import Optional
    >>> from dataclassish._src.converters import dataclass, field

    >>> @dataclass
    ... class MyClass:
    ...     attr: int | None = field(default=2.0, converter=Optional(int))

    The converter is applied to the default value:

    >>> MyClass().attr
    2

    The converter is applied to the input value:

    >>> MyClass(None).attr is None
    True

    >>> MyClass(1).attr
    1

    And will work for any input value that the converter can handle, e.g.
    ``int(str)``:

    >>> MyClass("3").attr
    3

    """
    if cls is None:
        return functools.partial(_process_dataclass, **kwargs)
    return _process_dataclass(cls, **kwargs)
