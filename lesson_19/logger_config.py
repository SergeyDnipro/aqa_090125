from pathlib import Path


BASE_DIR = Path(__file__).parent
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,  # Ensures only specified loggers are active
    "formatters": {
        "uni_formatter": {
            "format": "[%(asctime)s][%(levelname)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "nasa_images_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "uni_formatter",
            "filename": str(BASE_DIR / "parse_images.log"),
        },
        "flask_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "uni_formatter",
            "filename": str(BASE_DIR / "flask_debug.log"),
        },
    },
    "loggers": {
        "nasa_images_logger": {
            "level": "INFO",
            "handlers": ["nasa_images_handler"],
            "propagate": False,
        },
        "flask_logger": {
            "level": "INFO",
            "handlers": ["flask_handler"],
            "propagate": False,
        },
    },
    "root": {"level": "DEBUG", "handlers": []},
}