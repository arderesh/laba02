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