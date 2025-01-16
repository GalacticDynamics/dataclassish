"""Test `dataclass.converters`."""

import pytest

import dataclassish
from dataclassish._src.converters import dataclass, field


def test_abstractconverter_is_abstract():
    """Test `AbstractConverter` is abstract."""
    with pytest.raises(TypeError):
        _ = dataclassish.converters.AbstractConverter()


def test_optional_object():
    """Test `Optional` as an object."""
    converter = dataclassish.converters.Optional(int)

    assert converter(None) is None
    assert converter(1) == 1
    assert converter(1.0) == 1
    assert converter("1") == 1


def test_unless_object():
    """Test `Unless` as an object."""
    converter = dataclassish.converters.Unless(int, float)

    # Integers pass through
    assert isinstance(converter(1), int)
    assert converter(1) == 1

    # Everything else is converted to float
    assert isinstance(converter(1.0), float)
    assert converter(1.0) == 1.0
    assert converter("1") == 1.0
    assert converter("1.0") == 1.0


def test_field():
    """Test `field`."""
    converter = dataclassish.converters.Optional(int)

    # Normal usage
    f = field(converter=converter)
    assert f.metadata["converter"] is converter
    assert f.metadata["converter"](None) is None
    assert f.metadata["converter"](1.0) == 1

    # Non-callable converter
    with pytest.raises(TypeError, match="converter must be callable"):
        _ = field(converter=1)

    # converter also in metadata
    with pytest.raises(
        ValueError,
        match="cannot specify 'converter' in metadata and as a keyword argument.",
    ):
        _ = field(converter=converter, metadata={"converter": 1})

    # Converter is None
    f = field(converter=None)
    assert "converter" not in f.metadata

    # Converter is None, metadata is not None
    f = field(converter=None, metadata={"converter": converter})
    assert f.metadata["converter"] is converter
    assert f.metadata["converter"](None) is None
    assert f.metadata["converter"](1.0) == 1


def test_dataclass_with_converter():
    """Test `dataclass` with a converter field."""

    @dataclass(frozen=True, slots=True)
    class MyClass:
        attr: int | None = field(
            default=2.0, converter=dataclassish.converters.Optional(int)
        )

    # Test default value conversion
    obj = MyClass()
    assert obj.attr == 2

    # Test input value conversion
    obj = MyClass(None)
    assert obj.attr is None

    obj = MyClass(1)
    assert obj.attr == 1

    obj = MyClass("3")
    assert obj.attr == 3


def test_dataclass_skip_convert():
    """Test `dataclass` with `_skip_convert` flag."""

    @dataclass(frozen=True, slots=True)
    class MyClass:
        attr: int | None = field(
            default=2.0, converter=dataclassish.converters.Optional(int)
        )

    # Test skipping conversion
    obj = MyClass("3", _skip_convert=True)
    assert obj.attr == "3"


def test_dataclass_with_field_descriptor():
    """Test `dataclass` with a field descriptor."""

    class Descriptor:
        def __get__(self, instance, owner):
            return 42

    @dataclass(frozen=True, slots=True)
    class MyClass:
        attr: int = field(default=0, converter=int)
        descriptor: int = Descriptor()

    obj = MyClass()
    assert obj.attr == 0
    assert obj.descriptor == 42

    obj = MyClass(attr=1.0)
    assert obj.attr == 1
    assert obj.descriptor == 42


def test_dataclass_with_missing_mandatory_field():
    """Test `dataclass` with a missing mandatory field."""

    @dataclass(frozen=True, slots=True)
    class MyClass:
        attr: int | None = field()

    with pytest.raises(TypeError, match="missing 1 required positional argument"):
        _ = MyClass()
