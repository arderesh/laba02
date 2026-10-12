import csv
import json
from datetime import datetime
from collections.abc import Iterator

import logging
from streamstats.errors import InvalidEventError, InvalidTimestmpError, StreamStatsError
from streamstats.models import ALLOWED_LEVELS, Event


def make_event(data: dict[str, object], filename: str, line_number: int) -> Event:
    required_fields = {"timestamp", "level", "source", "message"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise InvalidEventError(f"В файле {filename} на строке {line_number} "
        f"нет обязательных полей {' '.join(sorted(missing_fields))}!")

    timestamp_val = data["timestamp"]
    level_val = data["level"]
    source_val = data["source"]
    message_val = data["message"]

    if not isinstance(timestamp_val, str):
        raise InvalidTimestmpError(f"В файле {filename} на строке {line_number} "
        f"метка {timestamp_val} не является строкой!")

    try:
        timestamp = datetime.fromisoformat(timestamp_val)
    except ValueError:
        raise InvalidTimestmpError(f"В файле {filename} на строке {line_number} "
                                   f"{timestamp_val}!")
    if not isinstance(level_val, str) or level_val not in ALLOWED_LEVELS:
        raise InvalidEventError(f"В файле {filename} на строке {line_number} "
                                f"некорректный уровень {level_val}!")

    if not isinstance(source_val, str) or not source_val.strip():
        raise InvalidEventError(f"В файле {filename} на строке {line_number} "
                                f"source не должно быть пустым!")

    if not isinstance(message_val, str):
        raise InvalidEventError(f"В файле {filename} на строке {line_number} "
                                f"message должно быть строкой!")

    return Event(timestamp=timestamp, level=level_val, source=source_val,
                 message=message_val)


def parse_csv(path: str, skip_invalid: bool = False) -> Iterator[Event | None]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                event = make_event(row, path, reader.line_num)
            except StreamStatsError as error:
                if not skip_invalid:
                    raise

                logging.warning(error)
                yield None
                continue

            yield event


def parse_jsonl(path: str, skip_invalid: bool = False) -> Iterator[Event | None]:
    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                data = json.loads(line)

                if not isinstance(data, dict):
                    raise InvalidEventError(f"В файле {path} на строке {line_number} "
                                            f"JSON должен содержать объект!")
                event = make_event(data, path, line_number)
            except json.JSONDecodeError:
                error = InvalidEventError(f"В файле {path} на строке {line_number} "
                                          f"некорректный JSON!")
                if not skip_invalid:
                    raise error
                logging.warning(error)
                yield None
                continue

            except StreamStatsError as e:
                if not skip_invalid:
                    raise

                logging.warning(e)
                yield None
                continue

            yield event
