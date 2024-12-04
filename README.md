<h1 align='center'> dataclassish </h1>
<h3 align="center">Tools from <code>dataclasses</code>, extended to all of Python</h3>

<p align="center">
    <a href="https://pypi.org/project/dataclassish/"> <img alt="PyPI: dataclassish" src="https://img.shields.io/pypi/v/dataclassish?style=flat" /> </a>
    <a href="https://pypi.org/project/dataclassish/"> <img alt="PyPI versions: dataclassish" src="https://img.shields.io/pypi/pyversions/dataclassish" /> </a>
    <a href="https://pypi.org/project/dataclassish/"> <img alt="dataclassish license" src="https://img.shields.io/github/license/GalacticDynamics/dataclassish" /> </a>
</p>
<p align="center">
    <a href="https://github.com/GalacticDynamics/dataclassish/actions"> <img alt="CI status" src="https://github.com/GalacticDynamics/dataclassish/workflows/CI/badge.svg" /> </a>
    <a href="https://codecov.io/gh/GalacticDynamics/dataclassish"> <img alt="codecov" src="https://codecov.io/gh/GalacticDynamics/dataclassish/graph/badge.svg" /> </a>
    <a href="https://scientific-python.org/specs/spec-0000/"> <img alt="ruff" src="https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038" /> </a>
    <a href="https://docs.astral.sh/ruff/"> <img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" /> </a>
    <a href="https://pre-commit.com"> <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" /> </a>
</p>

---

Python's [`dataclasses`][dataclasses-link] provides tools for working with
objects, but only compatible `@dataclass` objects. 😢 </br> This repository is a
superset of those tools and extends them to work on ANY Python object you want!
🎉 </br> You can easily register in object-specific methods and use a unified
interface for object manipulation. 🕶️

For example,

```{code-block} python
from dataclassish import replace  # New object, replacing select fields

d1 = {"a": 1, "b": 2.0, "c": "3"}
d2 = replace(d1, c=3 + 0j)
print(d2)
# {'a': 1, 'b': 2.0, 'c': (3+0j)}
```

## Installation

[![PyPI platforms][pypi-platforms]][pypi-link]
[![PyPI version][pypi-version]][pypi-link]

```bash
pip install dataclassish
```

## Documentation

- [Installation](#installation)
- [Documentation](#documentation)
  - [Getting Started](#getting-started)
    - [Working with a `@dataclass`](#working-with-a-dataclass)
    - [Working with a `dict`](#working-with-a-dict)
    - [The `__replace__` Method](#the-__replace__-method)
    - [Registering in a Custom Type](#registering-in-a-custom-type)
  - [Adding a Second Argument](#adding-a-second-argument)
  - [dataclass tools](#dataclass-tools)
  - [More tools](#more-tools)
  - [Converters](#converters)
  - [Flags](#flags)
- [Citation](#citation)
- [Development](#development)

### Getting Started

#### Working with a `@dataclass`

In this example we'll show how `dataclassish` works exactly the same as
[`dataclasses`][dataclasses-link] when working with a `@dataclass` object.

```{code-block} python
>>> from dataclassish import replace
>>> from dataclasses import dataclass

>>> @dataclass(frozen=True)
... class Point:
...     x: float | int
...     y: float | int


>>> p = Point(1.0, 2.0)
>>> p
Point(x=1.0, y=2.0)

>>> p2 = replace(p, x=3.0)
>>> p2
Point(x=3.0, y=2.0)
```

#### Working with a `dict`

Now we'll work with a [`dict`][dict-link] object. Note that
[`dataclasses`][dataclasses-link] does _not_ work with [`dict`][dict-link]
objects, but with `dataclassish` it's easy!

```{code-block} python
>>> from dataclassish import replace

>>> p = {"x": 1, "y": 2.0}
>>> p
{'x': 1, 'y': 2.0}

>>> p2 = replace(p, x=3.0)
>>> p2
{'x': 3.0, 'y': 2.0}

# If we try to `replace` a value that isn't in the dict, we'll get an error
>>> try:
...     replace(p, z=None)
... except ValueError as e:
...     print(e)
invalid keys {'z'}.
```

#### The `__replace__` Method

In Python 3.13+ objects can implement the `__replace__` method to define how
`copy.replace` should operate on them. This was directly inspired by
`dataclass.replace`, and is a nice generalization to more general Python
objects. `dataclassish` too supports this method.

```{code-block} python
>>> class HasReplace:
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...     def __repr__(self) -> str:
...         return f"HasReplace(a={self.a},b={self.b})"
...     def __replace__(self, **changes):
...         return type(self)(**(self.__dict__ | changes))

>>> obj = HasReplace(1, 2)
>>> obj
HasReplace(a=1,b=2)

>>> obj2 = replace(obj, b=3)
>>> obj2
HasReplace(a=1,b=3)

```

#### Registering in a Custom Type

Let's say there's a custom object that we want to use `replace` on, but which
doesn't have a `__replace__` method (or which we want more control over using a
second argument, discussed later). Registering in a custom type is very easy!
Let's make a custom object and define how `replace` will operate on it.

```{code-block} python
>>> from typing import Any
>>> from plum import dispatch

>>> class MyClass:
...     def __init__(self, a, b, c):
...         self.a = a
...         self.b = b
...         self.c = c
...     def __repr__(self) -> str:
...         return f"MyClass(a={self.a},b={self.b},c={self.c})"


>>> @dispatch
... def replace(obj: MyClass, **changes: Any) -> MyClass:
...     current_args = {k: getattr(obj, k) for k in "abc"}
...     updated_args = current_args | changes
...     return MyClass(**updated_args)


>>> obj = MyClass(1, 2, 3)
>>> obj
MyClass(a=1,b=2,c=3)

>>> obj2 = replace(obj, c=4.0)
>>> obj2
MyClass(a=1,b=2,c=4.0)
```

### Adding a Second Argument

`replace` can also accept a second positional argument which is a dictionary
specifying a nested replacement. For example consider the following dict of
Point objects:

```{code-block} python
>>> p = {"a": Point(1, 2), "b": Point(3, 4), "c": Point(5, 6)}
```

With `replace` the nested structure can be updated via:

```{code-block} python
>>> replace(p, {"a": {"x": 1.5}, "b": {"y": 4.5}, "c": {"x": 5.5}})
{'a': Point(x=1.5, y=2), 'b': Point(x=3, y=4.5), 'c': Point(x=5.5, y=6)}
```

In contrast in pure Python this would be very challenging. Expand the example
below to see how this might be done.

<details>
<summary>Expand for detailed example</summary>

This is a bad approach, updating the frozen dataclasses in place:

```{code-block} python
>>> from copy import deepcopy

>>> newp = deepcopy(p)
>>> object.__setattr__(newp["a"], "x", 1.5)
>>> object.__setattr__(newp["b"], "y", 4.5)
>>> object.__setattr__(newp["c"], "x", 5.5)
```

A better way might be to create an entirely new object!

```{code-block} python
>>> newp = {"a": Point(1.5, p["a"].y),
...         "b": Point(p["b"].x, 4.5),
...         "c": Point(5.5, p["c"].y)}
```

This isn't so good either.

</details>

`dataclassish.replace` is a one-liner that can work on any object (if it has a
registered means to do so), regardless of mutability or nesting. Consider this
fully immutable structure: And this is the simplest case, where the mutability
of a [`dict`][dict-link] allows us to copy the full object and update it after.
Note that we had to use
[`deepcopy`](https://docs.python.org/3/library/copy.html#copy.deepcopy) to avoid
mutating the sub-dicts. So what if the objects are immutable?

```{code-block} python
>>> @dataclass(frozen=True)
... class Object:
...     x: float | dict
...     y: float


>>> @dataclass(frozen=True)
... class Collection:
...     a: Object
...     b: Object


>>> p = Collection(Object(1.0, 2.0), Object(3.0, 4.0))
>>> p
Collection(a=Object(x=1.0, y=2.0), b=Object(x=3.0, y=4.0))

>>> replace(p, {"a": {"x": 5.0}, "b": {"y": 6.0}})
Collection(a=Object(x=5.0, y=2.0), b=Object(x=3.0, y=6.0))
```

With `replace` this remains a one-liner. Replace pieces of any structure,
regardless of nesting.

To disambiguate dictionary fields from nested structures, use the `F` marker.

```{code-block} python
>>> from dataclassish import F

>>> replace(p, {"a": {"x": F({"thing": 5.0})}})
Collection(a=Object(x={'thing': 5.0}, y=2.0),
           b=Object(x=3.0, y=4.0))
```

### dataclass tools

[`dataclasses`][dataclasses-link] has a number of utility functions beyond
`replace`: `fields`, `asdict`, and `astuple`. `dataclassish` supports of all
these functions.

```{code-block} python
>>> from dataclassish import fields, asdict, astuple

>>> p = Point(1.0, 2.0)

>>> fields(p)
(Field(name='x',...), Field(name='y',...))

>>> asdict(p)
{'x': 1.0, 'y': 2.0}

>>> astuple(p)
(1.0, 2.0)
```

`dataclassish` extends these functions to [`dict`][dict-link]'s:

```{code-block} python
>>> p = {"x": 1, "y": 2.0}

>>> fields(p)
(Field(name='x',...), Field(name='y',...))

>>> asdict(p)
{'x': 1, 'y': 2.0}

>>> astuple(p)
(1, 2.0)
```

Support for custom objects can be implemented similarly to `replace`.

### More tools

In addition to the `dataclasses` tools, `dataclassish` provides a few more
utilities.

- `get_field` returns the field of an object by name.
- `field_keys` returns the names of an object's fields.
- `field_values` returns the values of an object's fields.
- `field_items` returns the names and values of an object's fields.

### Converters

While `dataclasses.field` itself does not allow for converters (See PEP 712)
many dataclasses-like libraries do. A very short, very non-exhaustive list
includes: `attrs` and `equinox`. The module `dataclassish.converters` provides a
few useful converter functions. If you need more, check out `attrs`!

```{code-block} python
>>> from attrs import define, field
>>> from dataclassish.converters import Optional, Unless


>>> @define
... class Class1:
...     attr: int | None = field(default=None, converter=Optional(int))
...     """attr is converted to an int or kept as None."""


>>> obj = Class1()
>>> print(obj.attr)
None

>>> obj = Class1(attr=1.0)
>>> obj.attr
1

>>> @define
... class Class2:
...     attr: float | int = field(converter=Unless(int, converter=float))
...     """attr is converted to a float, unless it's an int."""

>>> obj = Class2(1)
>>> obj.attr
1

>>> obj = Class2("1")
>>> obj.attr
1.0
```

### Flags

`dataclassish` provides flags for customizing the behavior of functions. For
example, the [`coordinax`](https://pypi.org/project/coordinax/) package, which
depends on `dataclassish`, uses a flag `AttrFilter` to filter out fields from
consideration by the functions in `dataclassish`.

`dataclassish` provides a few built-in flags and flag-related utilities.

```{code-block} python
>>> from dataclassish import flags
>>> flags.__all__
['FlagConstructionError', 'AbstractFlag', 'NoFlag']
```

Where `AbstractFlag` is the base class for flags, and `NoFlag` is a flag that
does nothing. `FlagConstructionError` is an error that is raised when a flag is
constructed incorrectly.

As a quick example, we'll show how to use `NoFlag`.

```{code-block} python
>>> from dataclassish import field_keys
>>> field_keys(flags.NoFlag, p)
dict_keys(['x', 'y'])
```

## Citation

[![DOI][zenodo-badge]][zenodo-link]

If you enjoyed using this library and would like to cite the software you use
then click the link above.

## Development

[![Actions Status][actions-badge]][actions-link]
[![codecov][codecov-badge]][codecov-link]
[![SPEC 0 — Minimum Supported Dependencies][spec0-badge]][spec0-link]
[![pre-commit][pre-commit-badge]][pre-commit-link]
[![ruff][ruff-badge]][ruff-link]

We welcome contributions!

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/GalacticDynamics/dataclassish/workflows/CI/badge.svg
[actions-link]:             https://github.com/GalacticDynamics/dataclassish/actions
[codecov-badge]:            https://codecov.io/gh/GalacticDynamics/dataclassish/graph/badge.svg
[codecov-link]:             https://codecov.io/gh/GalacticDynamics/dataclassish
[pre-commit-badge]:         https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
[pre-commit-link]:          https://pre-commit.com
[pypi-link]:                https://pypi.org/project/dataclassish/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dataclassish
[pypi-version]:             https://img.shields.io/pypi/v/dataclassish
[rtd-badge]:                https://readthedocs.org/projects/dataclassish/badge/?version=latest
[rtd-link]:                 https://dataclassish.readthedocs.io/en/latest/?badge=latest
[ruff-badge]:               https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
[ruff-link]:                https://docs.astral.sh/ruff/
[spec0-badge]:              https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038
[spec0-link]:               https://scientific-python.org/specs/spec-0000/
[zenodo-badge]:             https://zenodo.org/badge/DOI/10.5281/zenodo.13357978.svg
[zenodo-link]:              https://zenodo.org/doi/10.5281/zenodo.13357978


[dataclasses-link]: https://docs.python.org/3/library/dataclasses.html
[dict-link]: https://docs.python.org/3.8/library/stdtypes.html#dict

<!-- prettier-ignore-end -->
