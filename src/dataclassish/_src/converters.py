"""Converters for dataclass fields.

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: ``attrs`` and ``equinox``. This module provides a few useful converter
functions. If you need more, check out ``attrs``!

"""
# ruff:noqa: N801

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
import sys
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Hashable, Mapping
from typing import (
    Any,
    ClassVar,
    Generic,
    Protocol,
    TypedDict,
    TypeVar,
    cast,
    overload,
)
from typing_extensions import NotRequired, dataclass_transform

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
            cast("PassThroughTs", value)
            if isinstance(value, self.unconverted_types)
            else self.converter(cast("ArgT", value))
        )


#####################################################################
# Minimal implementation of a dataclass supporting converters.

_CT = TypeVar("_CT")  # class type


# TODO: how to express default_factory is mutually exclusive with default?
if sys.version_info < (3, 12):
    DataclassFieldKwargsNotMetadata = Any

else:

    class DataclassFieldKwargsNotMetadata(TypedDict):
        """Keyword arguments for `dataclasses.field`."""

        default: NotRequired[object]
        init: NotRequired[bool]
        repr: NotRequired[bool]
        hash: NotRequired[bool | None]
        compare: NotRequired[bool]
        kw_only: NotRequired[bool]
        metadata: NotRequired[Mapping[Hashable, Any]]


def field(
    *,
    converter: Callable[[Any], Any] | None = None,
    metadata: Mapping[Hashable, Any] | None = None,
    **kwargs: DataclassFieldKwargsNotMetadata,
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


class DataclassWithConvertersInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]
    __dataclass_init__: Callable[..., None]
    __converter_init__: Callable[..., None]


def converter_init(
    self: DataclassWithConvertersInstance,
    args: tuple[Any],
    kwargs: dict[str, Any],
    *,
    _skip_convert: bool = False,
) -> None:
    # Fast path: no conversion
    if _skip_convert:
        self.__dataclass_init__(*args, **kwargs)
        return

    # Bind the arguments to the signature
    ba = self.__dataclass_init__._obj_signature_.bind_partial(*args, **kwargs)  # type: ignore[attr-defined]
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
    self.__dataclass_init__(*ba.args, **ba.kwargs)


def process_dataclass(cls: type[_CT], **dataclass_kwargs: Any) -> type[_CT]:
    """Process a class into a dataclass with converters.

    Parameters
    ----------
    cls : type
        The class to transform into a dataclass.
    **dataclass_kwargs : Any
        Additional keyword arguments to pass to `dataclasses.dataclass`.

    Returns
    -------
    type[DataclassInstance]
        The dataclass, it's a transformed version of the input class `cls`. This
        also adds the argument ``_skip_convert`` to the `__init__` method, which
        allows for skipping the conversion of fields. This provides a fast path
        for when the input values are already converted.

    """
    # Check if there's a user-defined __init__ method. If there is, we want this
    # to be the __init__ method of the dataclass as well. However, we need to
    # also get the dataclass-generated __init__ method, so we can call it later.
    # Therefore, we'll store the user's __init__, remove it, then add it back.
    has_custom_init = "__init__" in cls.__dict__
    custom_init = cls.__init__ if has_custom_init else None  # store for later
    if has_custom_init:  # rm, to ensure get dataclass __init__
        del cls.__init__

    # Make the dataclass from the class.
    # This does all the usual dataclass stuff.
    dataclass_kwargs["init"] = True
    dcls: type[_CT] = dataclasses.dataclass(cls, **dataclass_kwargs)

    # Store the dataclass-generated __init__ method
    dcls.__dataclass_init__ = dcls.__init__  # type: ignore[attr-defined]

    # Compute the signature of the dataclass-generated __init__ method and
    # eliminate the 'self' parameter since this will be used from the object,
    # not the class.
    sig = inspect.signature(dcls.__init__)
    sig = sig.replace(parameters=list(sig.parameters.values())[1:])

    # Add the converter init to the class. Also store the signature on the
    # method (Not assigning to __signature__ because that should have `self`).
    dcls.__converter_init__ = converter_init  # type: ignore[attr-defined]
    dcls.__dataclass_init__._obj_signature_ = sig  # type: ignore[attr-defined]

    # Assign the init method to the class. If there was a user-defined __init__
    # method, it is restored.
    if has_custom_init:
        init = custom_init
    else:

        @functools.wraps(dcls.__dataclass_init__)  # type: ignore[attr-defined]
        def init(
            self: DataclassWithConvertersInstance,
            *args: Any,
            _skip_convert: bool = False,
            **kwargs: Any,
        ) -> None:
            # Call the converter init method
            self.__converter_init__(args, kwargs, _skip_convert=_skip_convert)

    dcls.__init__ = init  # type: ignore[assignment]

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

    This function is a wrapper around `dataclasses.dataclass` that adds support
    for field converters. It does this by trying to access a converter function
    from the `dataclass.field` metadata for each field on the class. You can use
    the convenience function `dataclassish.converters.field` that handles adding
    a specified converter to the metadata. For more information about
    dataclasses see the `dataclasses` module.

    Converter-enabled dataclasses add two methods to the class:

    - `__dataclass_init__`: The original `__init__` method of the class.
    - `__converter_init__`: A wrapper for the `__dataclass_init__` method that
        handles argument conversion. This also supports the ``_skip_convert``
        argument, which will skip the conversion of the fields. This is useful
        for performance optimization. Note that the signature of this method is
        ``__converter_init__(self, args: tuple[Any], kwargs: dict[str, Any], *,
        _skip_convert: bool)``.

    If the class already has a user-defined `__init__` method, it will NOT be
    replaced. It is up to the user to ensure that the `__init__` method calls
    the `__converter_init__` method.

    Parameters
    ----------
    cls : type | None, optional
        The class to transform into a dataclass. If `None`, `dataclass` returns
        a partial function that can be used as a decorator.
    **kwargs : Any
        Additional keyword arguments to pass to `dataclasses.dataclass`.

    Examples
    --------
    >>> from dataclassish.converters import Optional
    >>> from dataclassish._src.converters import dataclass, field

    >>> @dataclass
    ... class Foo:
    ...     attr: int | None = field(default=2.0, converter=Optional(int))

    The converter is applied to the default value:

    >>> Foo().attr
    2

    The converter is applied to the input value:

    >>> Foo(None).attr is None
    True

    >>> Foo(1).attr
    1

    And will work for any input value that the converter can handle, e.g.
    ``int(str)``:

    >>> Foo("3").attr
    3

    If there already is a user-defined `__init__` method, it will not be
    replaced. It is up to the user to ensure that the `__init__` method calls
    the `__converter_init__` method.

    >>> @dataclass
    ... class Bar:
    ...     attr: int | None = field(default=2.0, converter=Optional(int))
    ...     def __init__(self, *, other_name: int | None) -> None:
    ...         self.__converter_init__((), {"attr": other_name})

    """
    if cls is None:
        return functools.partial(process_dataclass, **kwargs)
    return process_dataclass(cls, **kwargs)
