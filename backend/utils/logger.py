import logging
import os

LOG_DIR = "backend/logs"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=f"{LOG_DIR}/security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

security_logger = logging.getLogger("security_logger")