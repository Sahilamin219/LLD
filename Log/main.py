from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type

# Level constants (match stdlib logging)
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
LEVEL_NAMES = {DEBUG: "DEBUG", INFO: "INFO", WARNING: "WARNING", ERROR: "ERROR"}

# Simple in-memory config to choose handlers/levels per logger name.
# In a real app this could be loaded from JSON, env vars, or a file.
LOGGER_CONFIG: dict[str, dict[str, Any]] = {
    "payment": {
        "handler": "console_chain",  # or "console", "file", etc.
        "level": INFO,
    }
}


@dataclass
class LogRecord:
    """A single log event."""

    name: str
    levelno: int
    message: str
    formatted: str = ""

    @property
    def levelname(self) -> str:
        return LEVEL_NAMES.get(self.levelno, "NOTSET")


class LogFormatter(ABC):
    """Formats log records for output."""

    def format(self, name: str, level: int, message: str) -> LogRecord:
        formatted = self.format_message(name, level, message)
        return LogRecord(name=name, levelno=level, message=message, formatted=formatted)

    @abstractmethod
    def format_message(self, name: str, level: int, message: str) -> str:
        """Return the formatted log line string."""
        ...


class SimpleFormatter(LogFormatter):
    """Format: [LEVEL] name: message"""

    def format_message(self, name: str, level: int, message: str) -> str:
        levelname = LEVEL_NAMES.get(level, "NOTSET")
        return f"[{levelname}] {name}: {message}"


class LogHandler(ABC):
    """Chain-of-responsibility handler for log records."""

    def __init__(self, min_level: int = DEBUG, next_handler: "LogHandler | None" = None) -> None:
        self.min_level = min_level
        self.next_handler = next_handler

    def handle(self, record: LogRecord) -> None:
        # If this handler is interested in this level, emit it.
        if record.levelno >= self.min_level:
            self.emit(record)
        # Always pass down the chain so that e.g. ERROR also goes through INFO/DEBUG handlers.
        if self.next_handler is not None:
            self.next_handler.handle(record)

    @abstractmethod
    def emit(self, record: LogRecord) -> None:
        """Send the record to the destination (console, file, etc.)."""
        ...


class ConsoleHandler(LogHandler):
    """Prints log records to stdout."""

    def __init__(self, min_level: int = DEBUG, next_handler: "LogHandler | None" = None) -> None:
        super().__init__(min_level=min_level, next_handler=next_handler)

    def emit(self, record: LogRecord) -> None:
        print(record.formatted or f"[{record.levelname}] {record.name}: {record.message}")


class FileHandler(LogHandler):
    """Pretend file handler (demo)."""

    def __init__(self, min_level: int = DEBUG, next_handler: "LogHandler | None" = None) -> None:
        super().__init__(min_level=min_level, next_handler=next_handler)

    def emit(self, record: LogRecord) -> None:
        print("Writing to File:", record.formatted or f"[{record.levelname}] {record.name}: {record.message}")


def _build_level_chain(handler_cls: Type[LogHandler]) -> LogHandler:
    """Build a DEBUG→INFO→WARNING→ERROR chain using the given handler class.

    With this chain, an ERROR record will pass through all handlers and effectively
    be treated as ERROR, WARNING, INFO and DEBUG (because levelno >= min_level for each).
    """
    debug_handler = handler_cls(min_level=DEBUG)
    info_handler = handler_cls(min_level=INFO)
    warning_handler = handler_cls(min_level=WARNING)
    error_handler = handler_cls(min_level=ERROR)

    debug_handler.next_handler = info_handler
    info_handler.next_handler = warning_handler
    warning_handler.next_handler = error_handler

    return debug_handler


def create_handler_from_config(logger_name: str) -> LogHandler:
    """Create an appropriate handler (or chain) based on LOGGER_CONFIG."""
    cfg = LOGGER_CONFIG.get(logger_name, {})
    handler_type = cfg.get("handler", "console_chain")

    if handler_type == "console_chain":
        return _build_level_chain(ConsoleHandler)
    if handler_type == "console":
        return ConsoleHandler()
    if handler_type == "file":
        return FileHandler()
    # Fallback
    return ConsoleHandler()


class Log:
    def __init__(
        self,
        name: str,
        level: int | None = None,
        handler: LogHandler | None = None,
        formatter: LogFormatter | None = None,
    ) -> None:
        self.name = name
        # If level not explicitly provided, read from config; default to DEBUG.
        if level is None:
            level = LOGGER_CONFIG.get(name, {}).get("level", DEBUG)
        self.level = level
        # If handler not provided, build from config for this logger name.
        self.handler = handler or create_handler_from_config(name)
        self.formatter = formatter or SimpleFormatter()

    def setLevel(self, level: int) -> None:
        self.level = level

    def setHandler(self, handler: LogHandler) -> None:
        self.handler = handler

    def setFormatter(self, formatter: LogFormatter) -> None:
        self.formatter = formatter

    def log(self, level: int, message: str, *args: Any, **kwargs: Any) -> None:
        if level >= self.level:
            if args or kwargs:
                message = message.format(*args, **kwargs)
            record = self.formatter.format(self.name, level, message)
            self.handler.emit(record)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.log(DEBUG, message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.log(INFO, message, *args, **kwargs)

    def warn(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.log(WARNING, message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.log(ERROR, message, *args, **kwargs)


class LogFactory:
    """Creates configured Log instances."""

    def create_logger(
        self,
        name: str,
        level: int | None = None,
        handler: LogHandler | None = None,
        formatter: LogFormatter | None = None,
    ) -> Log:
        return Log(name, level=level, handler=handler, formatter=formatter)


# class LogAdapter:
#     """Thin adapter around a Log instance (e.g. for dependency injection)."""

#     def __init__(self, log: Log) -> None:
#         self._log = log

#     def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
#         self._log.debug(message, *args, **kwargs)

#     def info(self, message: str, *args: Any, **kwargs: Any) -> None:
#         self._log.info(message, *args, **kwargs)

#     def warn(self, message: str, *args: Any, **kwargs: Any) -> None:
#         self._log.warn(message, *args, **kwargs)

#     def error(self, message: str, *args: Any, **kwargs: Any) -> None:
#         self._log.error(message, *args, **kwargs)


class PaymentService:
    def __init__(self) -> None:
        # Handler and level for "payment" are now driven by LOGGER_CONFIG.
        self.log = LogFactory().create_logger("payment")

    def make_payment(self, amount: float) -> None:
        self.log.info(f"Making payment of {amount}")


if __name__ == "__main__":
    payment_service = PaymentService()
    payment_service.make_payment(100.0)
