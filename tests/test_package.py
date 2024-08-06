"""Test the package metadata."""

import importlib.metadata

import dataclassish as m


def test_version():
    """Test that the package version matches the metadata."""
    assert importlib.metadata.version("dataclassish") == m.__version__
