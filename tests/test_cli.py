import json
import subprocess
import sys

def test_cli_make_report(tmp_path):
    input_f = tmp_path / "events.jsonl"
    output_f = tmp_path / "report.json"

    input_f.write_text('{"timestamp":"2026-10-10T10:00:00", "level":"INFO",'
                       '"source":"app", "message":"Запуск"}\n', encoding="utf-8")

    result = subprocess.run([sys.executable, "-m", "streamstats", "analyze",
                             str(input_f), "--format", "jsonl", "--output",
                             str(output_f)], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stderr == ""
    assert output_f.exists()
    report = json.loads(output_f.read_text(encoding="utf-8"))

    assert report["total_events"] == 1
    assert report["by_level"] == {"INFO": 1}
    assert report["by_source"] == {"app": 1}


def test_skip_inval(tmp_path):
    input_f = tmp_path / "events.jsonl"
    output_f = tmp_path / "report.json"

    input_f.write_text('{"timestamp":"2026-10-10T10:00:00", "level":"INFO",'
                       '"source":"app", "message":"первая"}\n'
                       '{"timestamp":"неверная дата", "level":"ERROR",'
                       '"source":"app", "message":"поврежденная"}\n'
                       '{"timestamp":"2026-10-10T12:00:00", "level":"ERROR",'
                       '"source":"server", "message":"третья"}\n', encoding="utf-8")

    result = subprocess.run([sys.executable, "-m", "streamstats", "analyze",
                             str(input_f), "--format", "jsonl", "--output",
                             str(output_f), "--skip-invalid"], capture_output=True, text=True)

    assert result.returncode == 0
    report = json.loads(output_f.read_text(encoding="utf-8"))
    assert report["total_events"] == 2
    assert report["skipped_invalid"] == 1
    assert report["by_level"] == {"INFO": 1, "ERROR": 1}
    assert "WARNING" in result.stderr


def test_without_skip(tmp_path):
    input_f = tmp_path / "events.jsonl"
    output_f = tmp_path / "report.json"

    input_f.write_text('{"timestamp":"неверная дата",'
        '"level":"INFO", "source":"app", "message":"Ошибка"}\n', encoding="utf-8",)

    result = subprocess.run([sys.executable, "-m", "streamstats", "analyze",
                             str(input_f), "--format", "jsonl", "--output",
                             str(output_f)], capture_output=True, text=True)

    assert result.returncode == 2
    assert "на строке 1" in result.stderr
    assert not output_f.exists()


def test_2_input_f(tmp_path):
    frst = tmp_path / "first.jsonl"
    sec = tmp_path / "second.jsonl"
    output_f = tmp_path / "report.json"

    frst.write_text('{"timestamp":"2026-10-10T10:00:00", "level":"INFO", '
                    '"source":"app", "message":"Первое"}\n', encoding="utf-8")

    sec.write_text('{"timestamp":"2026-10-10T12:00:00", "level":"ERROR", '
                    '"source":"server", "message":"Второе"}\n', encoding="utf-8")

    result = subprocess.run([sys.executable, "-m", "streamstats", "analyze",
                             str(frst), str(sec), "--format", "jsonl", "--output",
                             str(output_f)], capture_output=True, text=True)

    assert result.returncode == 0

    report = json.loads(output_f.read_text(encoding="utf-8"))

    assert report["total_events"] == 2
    assert report["by_level"] == {"INFO": 1, "ERROR": 1}
    assert report["by_source"] == {"app": 1, "server": 1}
    assert report["first_timestamp"] == "2026-10-10T10:00:00"
    assert report["last_timestamp"] == "2026-10-10T12:00:00"


def test_miss_input_file(tmp_path):
    output_f = tmp_path / "report.json"
    miss_f = tmp_path / "missing.jsonl"

    result = subprocess.run([sys.executable, "-m", "streamstats", "analyze",
                             str(miss_f), "--format", "jsonl", "--output",
                             str(output_f)], capture_output=True, text=True)

    assert result.returncode == 2
    assert "missing.jsonl" in result.stderr
    assert not output_f.exists()