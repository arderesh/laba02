import csv
import json
from datetime import datetime

from streamstats.errors import InvalidEventError, InvalidTimestmpError
from streamstats.models import ALLOWED_LEVELS, Event


def make_event(data, filename, line_number):
    required_fields = {"timestamp", "level", "source", "message"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise InvalidEventError(filename, line_number, missing_fields)

    timestamp_val = data["timestamp"]
    level_val = data["level"]
    source_val = data["source"]
    message_val = data["message"]

    if not isinstance(timestamp_val, str):
        raise InvalidTimestmpError

    try:
        timestamp = datetime.fromisoformat(timestamp_val)
    except ValueError as error:
        raise InvalidTimestmpError

    if not isinstance(level_val, str) or level_val not in ALLOWED_LEVELS:
        raise InvalidEventError

    if not isinstance(source_val, str) or not source_val.strip():
        raise InvalidEventError

    if not isinstance(message_val, str):
        raise InvalidEventError

    return Event(timestamp=timestamp, level=level_val, source=source_val,
                 message=message_val)


def parse_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            yield make_event(row, path, reader.line_num)


def parse_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                raise InvalidEventError

            if not isinstance(data, dict):
                raise InvalidEventError

            yield make_event(data, path, line_number)
