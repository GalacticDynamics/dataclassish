<h1 align='center'> dataclassish </h1>
<h2 align="center">Tools from <code>dataclasses</code>, extended to all of Python</h2>

Python's [`dataclasses`][dataclasses-link] provides tools for working with
objects, but only compatible `@dataclass` objects. 😢 </br> This repository is a
superset of those tools and extends them to work on ANY Python object you want!
🎉 </br> You can easily register in object-specific methods and use a unified
interface for object manipulation. 🕶️

For example,

```python
from dataclassish import replace  # New object, replacing select fields

d1 = {"a": 1, "b": 2.0, "c": "3"}
d2 = replace(d1, c=3 + 0j)
print(d2)
# {'a': 1, 'b': 2.0, 'c': (3+0j)}
```

## Installation

[![PyPI platforms][pypi-platforms]][pypi-link]
[![PyPI version][pypi-version]][pypi-link]

<!-- [![Conda-Forge][conda-badge]][conda-link] -->

```bash
pip install dataclassish
```

## Documentation

[![Documentation Status][rtd-badge]][rtd-link]

WIP. But if you've worked with a
[`dataclass`](https://docs.python.org/3/library/dataclasses.html) then you
basically already know everything you need to know.

### Getting Started

In this example we'll show how `dataclassish` works exactly the same as
[`dataclasses`][dataclasses-link] when working with a `@dataclass` object.

```python
from dataclassish import replace
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


p = Point(1.0, 2.0)
print(p)
# Point(x=1.0, y=2.0)

p2 = replace(p, x=3.0)
print(p2)
# Point(x=3.0, y=2.0)
```

Now we'll work with a [`dict`][dict-link] object. Note that you cannot use tools
from [`dataclasses`][dataclasses-link] with [`dict`][dict-link] objects.

```python
from dataclassish import replace

p = {"x": 1, "y": 2.0}
print(p)
# {'x': 1, 'y': 2.0}

p2 = replace(p, x=3.0)
print(p2)
# {'x': 3.0, 'y': 2.0}

# If we try to `replace` a value that isn't in the dict, we'll get an error
try:
    replace(p, z=None)
except ValueError as e:
    print(e)
# invalid keys {'z'}.
```

Registering in a custom type is very easy! Let's make a custom object and define
how `replace` will operate on it.

```python
from typing import Any
from plum import dispatch


class MyClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self) -> str:
        return f"MyClass(a={self.a},b={self.b},c={self.c})"


@dispatch
def replace(obj: MyClass, **changes: Any) -> MyClass:
    current_args = {k: getattr(obj, k) for k in "abc"}
    updated_args = current_args | changes
    return MyClass(**updated_args)


obj = MyClass(1, 2, 3)
print(obj)
# MyClass(a=1,b=2,c=3)

obj2 = replace(obj, c=4.0)
print(obj2)
# MyClass(a=1,b=2,c=4.0)
```

### Adding a Second Argument

`replace` can also accept a second positional argument which is a dictionary
specifying a nested replacement. For example consider the following dict:

```python
p = {"a": {"a1": 1, "a2": 2}, "b": {"b1": 3, "b2": 4}, "c": {"c1": 5, "c2": 6}}
```

With `replace` the sub-dicts can be updated via:

```python
replace(p, {"a": {"a1": 1.5}, "b": {"b2": 4.5}, "c": {"c1": 5.5}})
# {'a': {'a1': 1.5, 'a2': 2}, 'b': {'b1': 3, 'b2': 4.5}, 'c': {'c1': 5.5, 'c2': 6}}
```

In contrast in pure Python this would be:

```python
from copy import deepcopy

newp = deepcopy(p)
newp["a"]["a1"] = 1.5
newp["b"]["b2"] = 4.5
newp["c"]["c1"] = 5.5
```

And this is the simplest case, where the mutability of a [`dict`][dict-link]
allows us to copy the full object and update it after. Note that we had to use
[`deepcopy`](https://docs.python.org/3/library/copy.html#copy.deepcopy) to avoid
mutating the sub-dicts. So what if the objects are immutable?

```python
@dataclass(frozen=True)
class Object:
    x: float | dict
    y: float


@dataclass(frozen=True)
class Collection:
    a: Object
    b: Object


p = Collection(Object(1.0, 2.0), Object(3.0, 4.0))
print(p)
Collection(a=Object(x=1.0, y=2.0), b=Object(x=3.0, y=4.0))

replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
# Collection(a=Object(x=5.0, y=2.0), b=Object(x=3.0, y=6.0))
```

With `replace` this remains a one-liner. Replace pieces of any structure,
regardless of nesting.

To disambiguate dictionary fields from nested structures, use the `F` marker.

```python
from dataclassish import F

replace(p, {"a": {"x": F({"thing": 5.0})}})
# Collection(a=Object(x={'thing': 5.0}, y=2.0),
#            b=Object(x=3.0, y=4.0))
```

### dataclass tools

[`dataclasses`][dataclasses-link] has a number of utility functions beyond
`replace`: `fields`, `asdict`, and `astuple`. `dataclassish` supports of all
these functions.

```python
from dataclassish import fields, asdict, astuple

p = Point(1.0, 2.0)

print(fields(p))
# (Field(name='x',...), Field(name='y',...))

print(asdict(p))
# {'x': 1.0, 'y': 2.0}

print(astuple(p))
# (1.0, 2.0)
```

`dataclassish` extends these functions to [`dict`][dict-link]'s:

```python
p = {"x": 1, "y": 2.0}

print(fields(p))
# (Field(name='x',...), Field(name='y',...))

print(asdict(p))
# {'x': 1.0, 'y': 2.0}

print(astuple(p))
# (1.0, 2.0)
```

Support for custom objects can be implemented similarly to `replace`.

### converters

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: `attrs` and `equinox`. The module `dataclassish.converters` provides a
few useful converter functions. If you need more, check out `attrs`!

```python
from attrs import define, field
from dataclassish.converters import Optional, Unless


@define
class Class1:
    attr: int | None = field(default=None, converter=Optional(int))


obj = Class1()
print(obj.attr)
# None

obj = Class1(a=1)
print(obj.attr)
# 1


@define
class Class2:
    attr: float | int = field(converter=Unless(int, converter=float))


obj = Class2(1)
print(obj.attr)
# 1

obj = Class2("1")
print(obj.attr)
# 1.0
```

## Citation

[![DOI][zenodo-badge]][zenodo-link]

If you enjoyed using this library and would like to cite the software you use
then click the link above.

## Development

[![Actions Status][actions-badge]][actions-link]

We welcome contributions!

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/GalacticDynamics/dataclassish/workflows/CI/badge.svg
[actions-link]:             https://github.com/GalacticDynamics/dataclassish/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/dataclassish
[conda-link]:               https://github.com/conda-forge/dataclassish-feedstock
[pypi-link]:                https://pypi.org/project/dataclassish/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dataclassish
[pypi-version]:             https://img.shields.io/pypi/v/dataclassish
[rtd-badge]:                https://readthedocs.org/projects/dataclassish/badge/?version=latest
[rtd-link]:                 https://dataclassish.readthedocs.io/en/latest/?badge=latest
[zenodo-badge]:             https://zenodo.org/badge/829828449.svg
[zenodo-link]:              https://zenodo.org/doi/10.5281/zenodo.13357978


[dataclasses-link]: https://docs.python.org/3/library/dataclasses.html
[dict-link]: https://docs.python.org/3.8/library/stdtypes.html#dict

<!-- prettier-ignore-end -->
