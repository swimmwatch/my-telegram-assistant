"""
Common configuration.
"""
from enum import Enum

from pydantic import BaseSettings


class RunLevelEnum(Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class BaseConfig:
    env_file_encoding = "utf-8"
    extra = "ignore"
    env_file = (".env", ".env.local")


class RunLevelBaseConfigMixin(BaseSettings):
    run_level: RunLevelEnum = RunLevelEnum.DEVELOPMENT
