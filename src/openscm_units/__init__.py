"""
Handling of units related to simple climate modelling.
"""
import importlib.metadata

from ._unit_registry import ScmUnitRegistry

__version__ = importlib.metadata.version("openscm_units")

__all__ = [
    "ScmUnitRegistry",
    "unit_registry",
]


unit_registry = ScmUnitRegistry()
"""
Standard unit registry

The unit registry contains all of the recognised units. Be careful, if you
edit this registry in one place then it will also be edited in any other
places that use :mod:`openscm_units`. If you want multiple, separate registries,
create multiple instances of :class:`ScmUnitRegistry`.
"""
unit_registry.add_standards()
