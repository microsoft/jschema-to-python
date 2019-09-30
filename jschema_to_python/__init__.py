import pbr
from pbr.version import VersionInfo

__version__ = VersionInfo(__package__).semantic_version().release_string()
