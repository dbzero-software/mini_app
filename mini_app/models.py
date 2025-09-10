"""
Mini App initialization module.
Creates a simple model to initialize the DBZero workspace.
"""

from dataclasses import dataclass
import dbzero_ce as db0
from mini_app.config import DATA_PREFIX


@db0.memo(prefix=DATA_PREFIX, singleton=True)
@dataclass
class MiniAppData:
    """
    Simple data model to initialize the DBZero workspace.
    This singleton class ensures the workspace is created.
    """
    app_name: str = "Mini App"
    version: str = "0.1.0"
    initialized: bool = True


def initialize_mini_app() -> MiniAppData:
    """
    Initialize the Mini App data model and DBZero workspace.
    
    Returns:
        MiniAppData: The initialized Mini App data singleton.
    """
    return MiniAppData()
