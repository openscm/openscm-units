"""
OpenSCM Units, units for use with simple climate modelling
"""
from ._version import get_versions
from .unit_registry import unit_registry  # noqa: F401

__version__ = get_versions()["version"]
del get_versions
