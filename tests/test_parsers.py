import json
import pytest

from streamstats.errors import InvalidEventError, InvalidTimestmpError
from streamstats.parsers import parse_csv, parse_jsonl


def test_csv(tmp_path):
    input_f = tmp_path / "events.csv"

    input_f.write_text("timestamp,level,source,message\n2026-10-10T10:00:00,INFO,app,Запуск\n",
                       encoding="utf-8")

    events = list(parse_csv(str(input_f)))

    assert len(events) == 1
    assert events[0].level == "INFO"
    assert events[0].source == "app"
    assert events[0].message == "Запуск"


def test_jsonl(tmp_path):
    input_f = tmp_path / "events.jsonl"

    input_f.write_text(json.dumps({"timestamp": "2026-10-10T10:00:00",
                                   "level": "ERROR",
                                   "source": "server",
                                   "message": "Ошибка"},
                                  ensure_ascii=False) + "\n", encoding="utf-8")
    events = list(parse_jsonl(str(input_f)))

    assert len(events) == 1
    assert events[0].level == "ERROR"
    assert events[0].source == "server"
    assert events[0].message == "Ошибка"


def test_empty_json(tmp_path):
    input_f = tmp_path / "events.jsonl"
    input_f.write_text("", encoding="utf-8")

    events = list(parse_jsonl(str(input_f)))

    assert events == []


def test_empty_csv(tmp_path):
    input_f = tmp_path / "events.csv"
    input_f.write_text("", encoding="utf-8")

    events = list(parse_csv(str(input_f)))

    assert events == []


def test_invalid_time(tmp_path):
    input_f = tmp_path / "events.jsonl"
    input_f.write_text('{"timestamp":"неверная дата",'
        '"level":"INFO",'
        '"source":"app",'
        '"message":"Тест"}\n', encoding="utf-8")

    with pytest.raises(InvalidTimestmpError) as error:
        list(parse_jsonl(str(input_f)))

    assert "на строке 1" in str(error.value)
    assert "неверная дата" in str(error.value)


def test_invalid_json(tmp_path):
    input_f = tmp_path / "events.jsonl"
    input_f.write_text('{"timestamp":"2026-10-10T10:00:00"\n', encoding="utf-8")

    with pytest.raises(InvalidEventError) as error:
        list(parse_jsonl(str(input_f)))

    assert "на строке 1" in str(error.value)
    assert "некорректный JSON" in str(error.value)


def test_invalid_json_rep_line_n(tmp_path):
    input_f = tmp_path / "events.jsonl"
    lines = ['{"timestamp":"2026-10-10T10:00:00",'
             '"level":"INFO","source":"app","message":"ok"}\n'] * 6
    lines.append("неверный json\n")

    input_f.write_text("".join(lines), encoding="utf-8")

    with pytest.raises(InvalidEventError) as error:
        list(parse_jsonl(str(input_f)))

    assert "на строке 7" in str(error.value)
