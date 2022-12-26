from datetime import date

from pydantic import BaseModel
from core.config import config


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "cobo-app-logger"
    LOG_FORMAT: str = (
        "%(levelprefix)s [%(asctime)s] [%(levelname)s] [%(name)s\t| %(message)s]"
    )
    LOG_FILE_FORMAT: str = "[%(asctime)s]\t-\t[%(levelname)s][%(name)s]\t::[%(module)s]|[%(lineno)s]:: %(message)s"
    ERROR_LOG_FORMAT: str = "[%(asctime)s]\t-\t[%(process)d]\t[%(levelname)s]-[%(name)s]::[%(module)s]|[%(lineno)s]:: %(message)s"
    LOG_LEVEL: str = "DEBUG" if config.DEBUG else "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "log_file_format": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FILE_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "error_log_format": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": ERROR_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "info_rotating_file_handler": {
            "level": "INFO",
            "formatter": "log_file_format",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"logs/{date.today()}/{date.today()}-info.log",
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 10,
        },
        "error_file_handler": {
            "level": "WARNING",
            "formatter": "error_log_format",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"logs/{date.today()}/{date.today()}-error.log",
            "mode": "a",
        },
        "critical_file_handler": {
            "level": "CRITICAL",
            "formatter": "error_log_format",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"logs/{date.today()}/{date.today()}-critical.log",
            "mode": "a",
        },
        # "critical_mail_handler": {
        #     "level": "CRITICAL",
        #     "formatter": "error",
        #     "class": "logging.handlers.SMTPHandler",
        #     "mailhost": "localhost",
        #     "fromaddr": "pr9.playbook88@gmail.com",
        #     "toaddrs": ["pr9.playbook88@gmail.com"],
        #     "subject": "Critical error with application name",
        # },
    }
    loggers = {
        f"": {
            "handlers": [
                "default",
                "info_rotating_file_handler",
                "error_file_handler",
                "critical_file_handler",
            ],
            "level": LOG_LEVEL,
        },
    }
