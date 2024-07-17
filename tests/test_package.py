"""Test the package metadata."""

import importlib.metadata

import dataclasstools as m


def test_version():
    """Test that the package version matches the metadata."""
    assert importlib.metadata.version("dataclasstools") == m.__version__
