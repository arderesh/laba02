import json

from streamstats.analysis import Statistics


def make_report(statistics: Statistics) -> dict:
    return {"total_events": statistics.total_evs,
            "by_level": dict(statistics.level),
            "by_source": dict(statistics.source),
            "top_error_sources": [{"source": source, "count": count}
                                  for source, count in statistics.top_errors()],
            "first_timestamp": (statistics.frst_timestmp.isoformat()
                                if statistics.frst_timestmp is not None else None),
            "last_timestamp": (statistics.last_timestmp.isoformat()
                               if statistics.last_timestmp is not None else None),
            "skipped_invalid": statistics.skip_invalid}


def save_report(report: dict, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
