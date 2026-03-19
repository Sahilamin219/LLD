from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime as dt

# Level order: DEBUG < INFO < WARNING < ERROR (higher = more severe)
LEVEL_SEVERITY = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}
LEVEL_ORDER = ["DEBUG", "INFO", "WARNING", "ERROR"]


@dataclass
class LogRecord:
    name: str
    level: str
    message: str

    def format_record(self, handler_level: str) -> str:
        return f"TimeStamp: {dt.datetime.now()} = [{self.name}] [{handler_level}] {self.message}"

    @property
    def level_no(self) -> int:
        return LEVEL_SEVERITY.get(self.level, 0)


class SinkHandler(ABC):
    def __init__(self, level: str, next_handler: "SinkHandler | None" = None):
        self.level = level
        self.next_handler = next_handler

    @abstractmethod
    def print_message(self, record: LogRecord) -> None:
        pass

    def call_next_handler(self, record: LogRecord) -> None:
        # print("call_next_handler", self.level)
        if self.next_handler is not None:
            # print("next_handler")
            self.next_handler.print_message(record)


class ConsoleHandler(SinkHandler):
    def __init__(self, level: str, next_handler: SinkHandler | None = None):
        super().__init__(level, next_handler)

    def print_message(self, record: LogRecord) -> None:
        # Only emit if record's level is at or above this handler's level
        if record.level_no >= LEVEL_SEVERITY.get(self.level, 0):
            print(f"record level {record.level_no}" ,record.format_record(self.level))
        self.call_next_handler(record)


class FileHandler(SinkHandler):
    def __init__(self, level: str, file_path: str, next_handler: SinkHandler | None = None):
        super().__init__(level, next_handler)
        self.file_path = file_path

    def print_message(self, record: LogRecord) -> None:
        if record.level_no >= LEVEL_SEVERITY.get(self.level, 0):
            with open(self.file_path, "a") as f:
                f.write(record.format_record(self.level) + "\n")
        self.call_next_handler(record)


class LoggerHandler:
    """Builds a chain of handlers from DEBUG up to the given handler's level."""

    @staticmethod
    def create_chain(handler: SinkHandler):
        handler_cls = type(handler)
        # print(handler_cls)
        top_level = handler.level
        if top_level not in LEVEL_ORDER:
            return handler
        # Build chain from tail (ERROR) to head (DEBUG) so head is the entry point
        top_idx = LEVEL_ORDER.index(top_level)
        levels_in_chain = LEVEL_ORDER[: top_idx + 1]  # e.g. ["DEBUG","INFO","WARNING","ERROR"]
        print(levels_in_chain)
        chain_tail = None
        for level in reversed(levels_in_chain):
            # Same sink type: ConsoleHandler needs no extra args; FileHandler needs file_path
            if handler_cls is FileHandler:
                file_path = getattr(handler, "file_path", "app.log")
                chain_tail = FileHandler(level, file_path, chain_tail)
            else:
                # print("level",level)
                chain_tail = handler_cls(level, chain_tail) # or chain_tail = ConsoleHandler(level, chain_tail)
            # print("chain" , type(chain_tail))
        return chain_tail
class Logger:
    def __init__(self, service_name: str, level: str, handler: SinkHandler):
        self.service_name = service_name
        self.level = level
        self.handler = handler
        self._chain = LoggerHandler.create_chain(handler)

    def log(self, message: str, level: str | None = None) -> None:
        log_level = level or self.level
        record = LogRecord(self.service_name, log_level, message)
        self._chain.print_message(record)


class LoggerFactory:
    @staticmethod
    def get_logger(service_name: str) -> Logger | None:
        if service_name == "PaymentService":
            return Logger(service_name, "ERROR", ConsoleHandler(level="ERROR")) # read from config for level
        return None


class PaymentService:
    payment_logger: Logger | None = LoggerFactory.get_logger("PaymentService")


if __name__ == "__main__":
    if PaymentService.payment_logger:
        PaymentService.payment_logger.log("This is a sample log message")
        # Log at ERROR: chain will pass record through DEBUG, INFO, WARNING, ERROR handlers
        # so you see one line (handler level that matches)
        # PaymentService.payment_logger.log("Payment failed", level="ERROR")
