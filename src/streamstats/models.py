from dataclasses import dataclass
from datetime import datetime

LEVELS_ALLOWED ={
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}

@dataclass(frozen=True)
class Event:
    timestamp: datetime
    level:str
    source: str
    message: str