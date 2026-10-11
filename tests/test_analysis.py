from datetime import datetime

from streamstats.analysis import Statistics, analyze_events
from streamstats.models import Event


def test_stats_cnt_evs():
    stats = Statistics()

    stats.add_event(Event(timestamp=datetime.fromisoformat("2026-10-10T10:00:00"),
                          level="INFO", source="app", message="Запуск"))
    stats.add_event(Event(timestamp=datetime.fromisoformat("2026-10-10T11:00:00"),
                          level="ERROR", source="server", message="Ошибка"))

    assert stats.total_evs == 2
    assert stats.level == {"INFO" : 1, "ERROR": 1}
    assert stats.source == {"app": 1, "server": 1}


def test_stats_frst_and_lst_time():
    stats = Statistics()

    stats.add_event(Event(timestamp=datetime.fromisoformat("2026-10-10T12:00:00"),
            level="INFO", source="app", message="Позднее событие"))
    stats.add_event(Event(timestamp=datetime.fromisoformat("2026-10-10T08:00:00"),
            level="INFO", source="app", message="Раннее событие"))

    assert stats.frst_timestmp == datetime.fromisoformat("2026-10-10T08:00:00")
    assert stats.last_timestmp == datetime.fromisoformat("2026-10-10T12:00:00")


def test_stats_cnts_e_sources():
    stats = Statistics()

    events = [Event(timestamp=datetime.fromisoformat("2026-10-10T10:00:00"),
            level="ERROR", source="server", message="Ошибка"),
        Event(timestamp=datetime.fromisoformat("2026-10-10T11:00:00"),
            level="CRITICAL", source="server", message="Крит ошибка"),
        Event(timestamp=datetime.fromisoformat("2026-10-10T12:00:00"),
            level="INFO", source="server", message="Инфо")]

    for event in events:
        stats.add_event(event)

    assert stats.err_sources == {"server": 2}


def test_top_errors():
    stats = Statistics()

    for source in ["b", "a", "c"]:
        stats.err_sources[source] = 2

    stats.err_sources["server"] = 5
    stats.err_sources["database"] = 3

    assert stats.top_errors() == [("server", 5), ("database", 3),
                                  ("a", 2), ("b", 2), ("c", 2)]


def test_analyze_events():
    events = [Event(timestamp=datetime.fromisoformat("2026-10-10T10:00:00"),
            level="INFO", source="app", message="Запуск"),
        Event(timestamp=datetime.fromisoformat("2026-10-10T11:00:00"),
            level="ERROR", source="server", message="Ошибка")]

    stats = analyze_events(events)

    assert stats.total_evs == 2
    assert stats.level == {"INFO": 1, "ERROR": 1}
