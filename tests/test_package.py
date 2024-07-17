from __future__ import annotations

import importlib.metadata

import dataclasstools as m


def test_version():
    assert importlib.metadata.version("dataclasstools") == m.__version__
