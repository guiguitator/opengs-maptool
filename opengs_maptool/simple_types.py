from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from logging import _nameToLevel

class TabName(Enum):
    # Values matter!
    LAND = "land"
    BOUNDARY = "boundary"
    DENSITY = "density"
    TERRAIN = "terrain"
    TERRITORY = "territory"
    PROVINCE = "province"

class LoggingLevel(Enum):
    # Get the logging-internal values as enum .value
    CRITICAL = _nameToLevel["CRITICAL"]
    FATAL = _nameToLevel["FATAL"]
    ERROR = _nameToLevel["ERROR"]
    WARNING = _nameToLevel["WARNING"]
    WARN = _nameToLevel["WARN"]
    INFO = _nameToLevel["INFO"]
    DEBUG = _nameToLevel["DEBUG"]
    NOTSET = _nameToLevel["NOTSET"]

    # Make the logging-internal values acecssible
    @property
    def logging_internal_value(self) -> int:
        return self.value
        # Alternative: getattr(logging, self.name)  # e.g., logging.INFO

@dataclass
class LoggerCategoryConfiguration:
    prefix: str
    level: LoggingLevel
    enabled: bool
