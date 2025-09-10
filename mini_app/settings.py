"""
Settings module for Mini App
Provides configuration management using Pydantic
"""

from typing import Optional
from enum import Enum
from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class InstanceType(Enum):
    """Type of database instance"""
    READONLY = "READONLY"
    RW = "R/W"


class MiniAppSettings(BaseSettings):
    """
    MiniAppSettings class - main configuration for the mini app.
    Configuration is retrieved from environment variables.
    """
    # Database configuration
    instance_type: InstanceType = InstanceType.RW
    cache_size: int = 1  # in GiB
    db_dir: str = "/mini_app_data/"
    
    # Application configuration
    app_name: str = "Mini App"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8080

    model_config = ConfigDict(env_file=".env")

    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty strings to None for proper validation"""
        return None if v == "" else v

    @field_validator("instance_type", mode="before")
    @classmethod
    def validate_instance_type(cls, v):
        """Validate instance type"""
        if isinstance(v, str):
            try:
                return InstanceType(v.upper())
            except ValueError:
                raise ValueError("Invalid instance type. Must be READONLY or R/W.")
        return v
