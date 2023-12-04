"""
Handling of units related to simple climate modelling.
"""
import importlib.metadata

from ._unit_registry import ScmUnitRegistry, unit_registry

__version__ = importlib.metadata.version("openscm_units")

__all__ = [
    "ScmUnitRegistry",
    "unit_registry",
]
