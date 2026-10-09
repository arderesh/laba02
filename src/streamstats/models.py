from dataclasses import dataclass
from datetime import datetime

ALLOWED_LEVELS ={
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}

@dataclass(frozen=True)
class Event:
    timestamp: datetime
    level: str
    source: str
    message: str