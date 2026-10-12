from datetime import datetime

from streamstats.analysis import Statistics
from streamstats.models import Event
from streamstats.report import make_report, save_report


def test_make_report():
    stats = Statistics()

    stats.add_event(Event(timestamp=datetime.fromisoformat("2026-10-10T10:00:00"),
            level="ERROR", source="server", message="Ошибка"))

    report = make_report(stats)
    assert report["total_events"] == 1
    assert report["by_level"] == {"ERROR": 1}
    assert report["by_source"] == {"server": 1}
    assert report["top_error_sources"] == [{"source": "server", "count": 1}]
    assert report["first_timestamp"] == "2026-10-10T10:00:00"
    assert report["last_timestamp"] == "2026-10-10T10:00:00"
    assert report["skipped_invalid"] == 0


def test_save_in_uni(tmp_path):
    output_f = tmp_path / "report.json"

    report = {"message": "Ошибка подкл",
              "source": "сервер"}

    save_report(report, str(output_f))

    content = output_f.read_text(encoding="utf-8")

    assert "Ошибка подкл" in content
    assert "сервер" in content
    assert "\\u" not in content


def test_empty_report():
    stats = Statistics()

    report = make_report(stats)

    assert report["total_events"] == 0
    assert report["by_level"] == {}
    assert report["by_source"] == {}
    assert report["top_error_sources"] == []
    assert report["first_timestamp"] is None
    assert report["last_timestamp"] is None
    assert report["skipped_invalid"] == 0
