<h1 align='center'> dataclasstools </h1>
<h2 align="center">Tools from dataclasses, extended to all of Python</h2>

Python's `dataclasses` provides tools for working with objects, but only
compatible `@dataclass` objects. 😢 </br> This repository is a superset of those
tools and extends them to work on ANY Python object you want! 🎉 </br> You can
easily register in object-specific methods and use a unified interface for
object manipulation. 🕶️

For example,

```python
from dataclasstools import replace  # New object, replacing select fields

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
pip install dataclasstools
```

## Documentation

[![Documentation Status][rtd-badge]][rtd-link]

WIP. But if you've worked with a
[`dataclass`](https://docs.python.org/3/library/dataclasses.html) then you
basically already know everything you need to know.

## Quick example

In this Example we'll show how `dataclasstools` works exactly the same as
`dataclasses` when working with a `@dataclass` object.

```python
from dataclasstools import replace
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

Now we'll work with a `dict` object. Note that you cannot use tools from
`dataclasses` with `dict` objects.

```python
from dataclasstools import replace

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

## Citation

[![DOI][zenodo-badge]][zenodo-link]

If you found this library to be useful in academic work, then please cite.

## Development

[![Actions Status][actions-badge]][actions-link]

We welcome contributions!

<!-- [![GitHub Discussion][github-discussions-badge]][github-discussions-link] -->

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/GalacticDynamics/dataclasstools/workflows/CI/badge.svg
[actions-link]:             https://github.com/GalacticDynamics/dataclasstools/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/dataclasstools
[conda-link]:               https://github.com/conda-forge/dataclasstools-feedstock
<!-- [github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/GalacticDynamics/dataclasstools/discussions -->
[pypi-link]:                https://pypi.org/project/dataclasstools/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dataclasstools
[pypi-version]:             https://img.shields.io/pypi/v/dataclasstools
[rtd-badge]:                https://readthedocs.org/projects/dataclasstools/badge/?version=latest
[rtd-link]:                 https://dataclasstools.readthedocs.io/en/latest/?badge=latest
[zenodo-badge]:             https://zenodo.org/badge/755708966.svg
[zenodo-link]:              https://zenodo.org/doi/10.5281/zenodo.10850557

<!-- prettier-ignore-end -->
