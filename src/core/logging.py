import logging
import logging.handlers
import os
import sys
from contextvars import ContextVar
from pathlib import Path

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [req=%(request_id)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())
    root.addHandler(handler)

    # Phase-2 observability: when WLS_LOG_FILE is set, also write to a
    # rotating file so Promtail can tail it and ship to Loki.
    file_path = os.environ.get("WLS_LOG_FILE")
    if file_path:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            file_path, maxBytes=50 * 1024 * 1024, backupCount=5, encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(RequestIdFilter())
        root.addHandler(file_handler)

    root.setLevel(level)

    for noisy in ("uvicorn.access",):
        logging.getLogger(noisy).setLevel(logging.WARNING)
