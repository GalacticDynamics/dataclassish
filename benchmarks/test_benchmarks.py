"""Benchmarks for `dataclassish`.

These benchmarks exercise the public, multiple-dispatch-based API of
``dataclassish`` across the different object types it supports (mappings and
dataclasses). They are collected and run by ``pytest-codspeed``.
"""

from dataclasses import dataclass

import pytest

from dataclassish import (
    asdict,
    astuple,
    field_items,
    field_keys,
    field_values,
    fields,
    get_field,
    replace,
)
from dataclassish.converters import (
    Optional,
    Unless,
    dataclass as converter_dataclass,
    field as converter_field,
)


@dataclass(frozen=True)
class Point:
    """A small dataclass used across the benchmarks."""

    x: int
    y: int
    z: int


def _make_mapping() -> dict[str, object]:
    return {"a": 1, "b": 2.0, "c": "3", "d": 4, "e": 5.0}


def _make_point() -> Point:
    return Point(1, 2, 3)


# ============================================================================
# Mapping dispatches


@pytest.mark.benchmark
def test_replace_mapping(benchmark: object) -> None:
    """Benchmark `replace` on a mapping."""
    d = _make_mapping()
    benchmark(lambda: replace(d, c=3 + 0j, d=40))


@pytest.mark.benchmark
def test_asdict_mapping(benchmark: object) -> None:
    """Benchmark `asdict` on a mapping."""
    d = _make_mapping()
    benchmark(lambda: asdict(d))


@pytest.mark.benchmark
def test_field_items_mapping(benchmark: object) -> None:
    """Benchmark `field_items` on a mapping."""
    d = _make_mapping()
    benchmark(lambda: field_items(d))


# ============================================================================
# Dataclass dispatches


@pytest.mark.benchmark
def test_replace_dataclass(benchmark: object) -> None:
    """Benchmark `replace` on a dataclass."""
    p = _make_point()
    benchmark(lambda: replace(p, x=10, z=30))


@pytest.mark.benchmark
def test_fields_dataclass(benchmark: object) -> None:
    """Benchmark `fields` on a dataclass."""
    p = _make_point()
    benchmark(lambda: fields(p))


@pytest.mark.benchmark
def test_asdict_dataclass(benchmark: object) -> None:
    """Benchmark `asdict` on a dataclass."""
    p = _make_point()
    benchmark(lambda: asdict(p))


@pytest.mark.benchmark
def test_astuple_dataclass(benchmark: object) -> None:
    """Benchmark `astuple` on a dataclass."""
    p = _make_point()
    benchmark(lambda: astuple(p))


@pytest.mark.benchmark
def test_get_field_dataclass(benchmark: object) -> None:
    """Benchmark `get_field` on a dataclass."""
    p = _make_point()
    benchmark(lambda: get_field(p, "y"))


@pytest.mark.benchmark
def test_field_keys_dataclass(benchmark: object) -> None:
    """Benchmark `field_keys` on a dataclass."""
    p = _make_point()
    benchmark(lambda: field_keys(p))


@pytest.mark.benchmark
def test_field_values_dataclass(benchmark: object) -> None:
    """Benchmark `field_values` on a dataclass."""
    p = _make_point()
    benchmark(lambda: field_values(p))


@pytest.mark.benchmark
def test_field_items_dataclass(benchmark: object) -> None:
    """Benchmark `field_items` on a dataclass."""
    p = _make_point()
    benchmark(lambda: field_items(p))


# ============================================================================
# Converters


@pytest.mark.benchmark
def test_converter_dataclass_construction(benchmark: object) -> None:
    """Benchmark constructing a converter-enabled dataclass."""

    @converter_dataclass(frozen=True, slots=True)
    class Model:
        a: int | None = converter_field(converter=Optional(int))
        b: float = converter_field(converter=Unless(float, float))

    benchmark(lambda: Model(a="1", b=2))
