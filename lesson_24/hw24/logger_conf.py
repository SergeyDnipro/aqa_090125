import logging.config
from pathlib import Path


BASE_DIR = Path(__file__).parent
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,  # Ensures only specified loggers are active
    "formatters": {
        "default_formatter": {
            "format": "[%(asctime)s][%(levelname)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "default_formatter",
            "filename": str(BASE_DIR / "test_search.log"),
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default_formatter",
        },
    },
    "loggers": {
        "car_app_logger": {
            "level": "INFO",
            "handlers": ["file_handler", "console_handler"],
            "propagate": False,
        },
    },
    "root": {"level": "DEBUG", "handlers": []},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("car_app_logger")
