"""Copyright (c) 2024 Nathaniel Starkman. All rights reserved.

Test dispatch resolution of the public API.

beartype 0.23 made ``TypeHint(Any) <= TypeHint(X)`` true for every ``X``, so
plum ranks ``Any``-typed methods as *more* specific than everything else.
Catch-all methods must therefore annotate with ``object``, not ``Any``.
"""

from dataclasses import dataclass, field
from typing import Any

import pytest

import dataclassish
from dataclassish.flags import AbstractFlag, FilterRepr, NoFlag

DISPATCHED = [
    getattr(dataclassish, name)
    for name in dataclassish.__all__
    if hasattr(getattr(dataclassish, name), "methods")
]


@pytest.mark.parametrize("func", DISPATCHED, ids=lambda f: f.__name__)
def test_no_bare_any_in_dispatch_signatures(func):
    """No registered method may dispatch on a bare `typing.Any`."""
    bad = [m.signature for m in func.methods if Any in m.signature.types]
    assert not bad, f"use `object` instead of `Any` in {bad}"


@dataclass
class Point:
    """A dataclass with a ``repr=False`` field."""

    x: int = 1
    y: int = field(default=2, repr=False)


def test_mapping_dispatch():
    """Mappings route to the Mapping methods, not the `getattr` fallback."""
    p = {"a": {"x": 1}, "b": 2}
    assert dataclassish.get_field(p, "a") == {"x": 1}
    assert dataclassish.replace(p, {"a": {"x": 3}}) == {"a": {"x": 3}, "b": 2}
    assert tuple(dataclassish.field_keys(p)) == ("a", "b")
    assert tuple(dataclassish.field_values(p)) == ({"x": 1}, 2)
    assert tuple(dataclassish.field_items(p)) == (("a", {"x": 1}), ("b", 2))


@pytest.mark.parametrize("obj", [Point(), {"x": 1, "y": 2}], ids=["dataclass", "dict"])
def test_noflag_dispatch(obj):
    """`NoFlag` is the same as passing no flag."""
    assert dataclassish.field_keys(NoFlag, obj) == dataclassish.field_keys(obj)
    assert dataclassish.asdict(NoFlag, obj) == {"x": 1, "y": 2}
    assert dataclassish.astuple(NoFlag, obj) == (1, 2)
    assert dataclassish.get_field(dataclassish.replace(NoFlag, obj, x=5), "x") == 5


def test_filterrepr_dispatch():
    """`FilterRepr` drops ``repr=False`` fields."""
    p = Point()
    assert dataclassish.field_keys(FilterRepr, p) == ("x",)
    assert dataclassish.field_values(FilterRepr, p) == (1,)
    assert dataclassish.field_items(FilterRepr, p) == (("x", 1),)
    assert dataclassish.asdict(FilterRepr, p) == {"x": 1}
    assert dataclassish.astuple(FilterRepr, p) == (1,)
    assert dataclassish.get_field(FilterRepr, p, "x") == 1


@pytest.mark.parametrize(
    "call",
    [
        lambda o: dataclassish.replace(AbstractFlag, o, x=5),
        lambda o: dataclassish.fields(AbstractFlag, o),
        lambda o: dataclassish.asdict(AbstractFlag, o),
        lambda o: dataclassish.astuple(AbstractFlag, o),
        lambda o: dataclassish.field_keys(AbstractFlag, o),
        lambda o: dataclassish.field_values(AbstractFlag, o),
        lambda o: dataclassish.field_items(AbstractFlag, o),
    ],
)
@pytest.mark.parametrize("obj", [Point(), {"x": 1, "y": 2}], ids=["dataclass", "dict"])
def test_abstractflag_raises(call, obj):
    """`AbstractFlag` itself is rejected."""
    with pytest.raises(ValueError, match="AbstractFlag"):
        call(obj)
