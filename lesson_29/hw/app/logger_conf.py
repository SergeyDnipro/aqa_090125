import logging
import os

os.makedirs('/app/logs', exist_ok=True)

logger = logging.getLogger("test_db_logger")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("/app/logs/test_db_features.log")],
)
