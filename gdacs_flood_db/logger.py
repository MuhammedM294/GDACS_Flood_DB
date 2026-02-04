import datetime as dt
import json
import os
import logging
from logging.handlers import SMTPHandler
import logging.config
from typing import override
from pathlib import Path
import concurrent_log_handler

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class MyJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO


def setup_logging():

    # Determine paths
    ROOT_DIR = Path(__file__).resolve().parents[1]
    config_file = ROOT_DIR / "logging_config.json"

    # Ensure log directory exists
    log_file = ROOT_DIR / "logs"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if config_file.exists():
        with open(config_file, "rt", encoding="utf8") as f:
            config_dict = json.load(f)

        # allow log level override via environment variable
        env_log_level = os.getenv("LOG_LEVEL")
        if env_log_level:
            config_dict["loggers"]["root"]["level"] = env_log_level.upper()
        logging.config.dictConfig(config_dict)
    else:
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", "INFO").upper(),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
