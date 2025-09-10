"""
Configuration module for Mini App
Handles DBZero configuration and application settings
"""

from functools import lru_cache
from mini_app.settings import MiniAppSettings


# Organization and project configuration
ORG_NAME = "miniapp"
PROJECT_NAME = "mini_app"
ENV = "dev"
DATA_PREFIX = f"/{ORG_NAME}/{PROJECT_NAME}/{ENV}/data"


@lru_cache()
def get_settings() -> MiniAppSettings:
    """
    Retrieve the application settings with caching.

    Returns:
        MiniAppSettings: An instance of the MiniAppSettings class containing the application configuration.
    """
    return MiniAppSettings()


def get_dbzero_config() -> dict:
    """
    Get DBZero configuration dictionary.
    
    Returns:
        dict: Configuration for DBZero connection
    """
    settings = get_settings()
    cache_size_bytes = settings.cache_size << 30  # Convert GiB to bytes
    
    print(f"Cache size set to {cache_size_bytes} bytes ({settings.cache_size} GiB)")
    
    return {
        "prefix": DATA_PREFIX,
        "autocommit": True,
        "autocommit_interval": 2000,
        "cache_size": cache_size_bytes,
        "db0_dir": settings.db_dir
    }
