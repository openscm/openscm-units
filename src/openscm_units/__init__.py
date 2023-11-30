"""
Handling of units related to simple climate modelling.
"""
import importlib.metadata

from .registry import ScmUnitRegistry, unit_registry  # noqa: F401

__version__ = importlib.metadata.version("openscm_units")
