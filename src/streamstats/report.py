import json
from typing import Any

from streamstats.analysis import Statistics


def make_report(statistics: Statistics):
    return {"total_events": statistics.total_evs,
            "level": dict(statistics.level),
            "source": dict(statistics.source),
            "top_error": [{"source": source,
                           "count": count} for source, count in statistics.top_errors()],
            "first_timestamp": (statistics.frst_timestmp.isoformat() if statistics.frst_timestmp is not None
                                else None),
            "last_timestamp": (statistics.last_timestmp.isoformat() if statistics.last_timestmp is not None
                               else None),
            "skip_invalid": statistics.skip_invalid}


