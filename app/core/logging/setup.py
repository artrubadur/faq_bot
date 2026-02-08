import logging
import sys
from pathlib import Path

import yaml
from loguru import logger

from app.core.logging.throttler import TelegramThrottler
from app.utils.format.log import serialize_json


def make_telegram_sink(log_manager: TelegramThrottler):
    def telegram_sink(message):
        record = message.record

        log_manager.add_log(
            record["name"] or "unknown",
            record["message"],
            record["level"],
            record["exception"],
        )

    return telegram_sink


def setup_logging(config_path: Path, cooldown: int):
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
            log_manager = TelegramThrottler(cooldown)
            sink = make_telegram_sink(log_manager)
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
