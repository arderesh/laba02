class StreamStatsError(Exception):
    """базовая ошибка аппки"""

class UnsupportedFileFormatError(StreamStatsError):
    """неподдерживаемый формат файла"""

class InvalidEventError(StreamStatsError):
    """неверное событие"""

class InvalidTimestmpError(StreamStatsError):
    """неверная временная метка"""

class CLIConfError(StreamStatsError):
    """ошибка конфигурации CLI"""