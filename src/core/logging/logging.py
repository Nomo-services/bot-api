import json
import logging
import os
import socket
import time

from fastapi import Request
from pythonjsonlogger import jsonlogger
from src.core.settings.settings import settings

SENSITIVE_KEYS = ["secret", "password", "data.password", "data.secret"]


def normalize_variables(data: any) -> str | None:
    if data is None:
        return None

    def mask_sensitive(d):
        if isinstance(d, dict):
            masked = {}
            for k, v in d.items():
                if k in SENSITIVE_KEYS:
                    masked[k] = "***"
                else:
                    masked[k] = mask_sensitive(v)
            return masked
        elif isinstance(d, list):
            return [mask_sensitive(item) for item in d]
        else:
            return d

    try:
        masked_data = mask_sensitive(data)
        return json.dumps(masked_data)
    except Exception:
        return str(data)


def get_req_logger_context(req: Request) -> dict[str, any]:
    context = {}
    context["reqId"] = getattr(req.state, "req_id", None)
    context["sessionId"] = req.cookies.get("sessionID")
    context["ip"] = req.client.host if req.client else None
    context["fingerprint"] = req.cookies.get("userId")
    context["complexity"] = getattr(req.state, "complexity", None)
    return context


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, json_ensure_ascii=False, **kwargs)
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        LEVEL_MAPPING = {
            logging.DEBUG: 10,
            logging.INFO: 30,
            logging.WARNING: 40,
            logging.ERROR: 50,
            logging.CRITICAL: 60,
        }
        log_record["level"] = LEVEL_MAPPING.get(record.levelno, record.levelno)
        log_record["timestamp"] = time.strftime(
            "%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)
        )
        log_record["pid"] = os.getpid()
        log_record["hostname"] = socket.gethostname()
        log_record["name"] = record.name


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    logger.handlers.clear()
    handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        fmt="%(levelname)s %(asctime)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_logger_options(name: str, req: Request) -> dict[str, any]:
    logger = get_logger(name)
    context = get_req_logger_context(req)
    return {"logger": logger, "custom_props": context}
