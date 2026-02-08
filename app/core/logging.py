import json
import logging
import sys
import traceback
from pathlib import Path

import yaml
from loguru import logger, Message

from app.dialogs.send.common import send_log
from app.services.notification import notify
from app.storage.models.user import Role
import asyncio
from contextvars import ContextVar

is_notifying = ContextVar("is_notifying", default=False)

def telegram_sink(message: Message):
    if is_notifying.get():
        return
    
    record = message.record

    loop = asyncio.get_event_loop()
    if loop.is_running():
        token = is_notifying.set(True)
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(notify(Role.ADMIN, send_log, record['name'], record['message'], record['level'], record['exception']))
        finally:
            is_notifying.reset(token)


def serialize_json(record):
    payload = {
        "time": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "name": record["name"],
    }
    exception = record["exception"]
    if exception:
        payload["error"] = "".join(
            traceback.format_exception(
                exception.type, exception.value, exception.traceback
            )
        )

    return f"{{{json.dumps(payload, ensure_ascii=False)}}}\n"


def setup_logging(config_path: Path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    logger.remove()

    for h in config.get("handlers", []):
        raw_sink = h.pop("sink")
        sink: str | sys.TextIO

        if raw_sink == "ext://sys.stdout":
            sink = sys.stdout
        elif raw_sink == "ext://sys.stderr":
            sink = sys.stderr
        elif raw_sink == "telegram":
            sink = telegram_sink
        else:
            sink = str(raw_sink)

        is_json = h.pop("json", False)

        if is_json:
            h["format"] = serialize_json

        logger.add(sink, **h, backtrace=True, diagnose=False)

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).patch(
                lambda r: r.update(name=record.name)
            ).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
