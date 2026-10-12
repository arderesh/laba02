# StreamStats

Анализатор событий из CSV- и JSONL-файлов. Программа
читает входные файлы, проверяет события, объединяет статистику и
сохраняет результат в JSON-отчёт.

## Формат события

Каждое событие содержит обязательные поля:

- `timestamp` - дата и время;
- `level` - уровень события: `DEBUG`, `INFO`, `WARNING`, `ERROR` или `CRITICAL`;
- `source` - непустая строка с названием источника;
- `message` - строка с текстом сообщения.


## Установка

```bash
python -m pip install -e . 
```

## Использование

Анализ CSV-файла:

```bash
python -m streamstats analyze events.csv --format csv --output report.json
```

Анализ JSONL-файла:

```bash
python -m streamstats analyze events.jsonl --format jsonl --output report.json
```

Можно передать несколько файлов одного формата:

```bash
python -m streamstats analyze first.jsonl second.jsonl --format jsonl --output report.json
```

## Обработка ошибок

При ошибке программа оснанавливает обрабтку, выводит имя файла и номер строки и 
завершает работу с кодом `2`.

Чтобы пропускать ошибочные строки и продолжать обработку, используется флаг `--skip-invalid`:

В этом режиме информация об ошибке записывается в лог с уровнем `WARNING`, а
количество пропущенных строк сохраняется в `skipped_invalid`.

## JSON-отчёт

Отчёт содержит следующие поля:

- `total_events` - кол-во корректных событий;
- `by_level` - кол-во событий каждого уровня;
- `by_source` - кол-во событий каждого источника;
- `top_error_sources` - топ-5 источников с наиб. кол-вом событий
  уровней `ERROR` и `CRITICAL`;
- `first_timestamp` - первая time метка;
- `last_timestamp` - последняя time метка;
- `skipped_invalid` - кол-во пропущенных ошибочных строк.

Пример отчёта:

```json
{
  "total_events": 2,
  "by_level": {
    "INFO": 1,
    "ERROR": 1
  },
  "by_source": {
    "app": 1,
    "server": 1
  },
  "top_error_sources": [
    {
      "source": "server",
      "count": 1
    }
  ],
  "first_timestamp": "2026-10-10T10:00:00",
  "last_timestamp": "2026-10-10T11:00:00",
  "skipped_invalid": 0
}
```

## Потоковая обработка

Во время анализа в памяти находятся счётчики уровней, источников и ошибок,
а также первая и последняя временные метки. 

## Проверка и тесты

```bash
python -m pytest
ruff check .
python -m streamstats --help
```
