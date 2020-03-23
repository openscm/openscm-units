from ._version import get_versions
from .unit_registry import unit_registry

__version__ = get_versions()["version"]
del get_versions
