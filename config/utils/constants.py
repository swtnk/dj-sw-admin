from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    LOGIN_FAILED: str = "Invalid Credentials"
    LOG_ROTATING_FILE_HANDLER_CLASS: str = "logging.handlers.RotatingFileHandler"
    LOG_STREAM_HANDLER_CLASS: str = "logging.StreamHandler"


@dataclass(frozen=True)
class LogLevel:
    CRITICAL: tuple = ("CRITICAL", 50)
    ERROR: tuple = ("ERROR", 40)
    WARNING: tuple = ("WARNING", 30)
    INFO: tuple = ("INFO", 20)
    DEBUG: tuple = ("DEBUG", 10)
    NOTSET: tuple = ("NOTSET", 0)


@dataclass(frozen=True)
class Messages:
    LOGIN_FAILED: str = "Invalid Credentials"
