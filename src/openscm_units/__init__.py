"""
OpenSCM Units, units for use with simple climate modelling
"""
from ._unit_registry import ScmUnitRegistry, unit_registry  # noqa: F401
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
