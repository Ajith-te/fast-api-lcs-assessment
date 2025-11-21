import os
import logging


# Create logs directory if it doesn't exist
LOG_DIR = "core/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "csv_processor.log")

# Create logger
logger = logging.getLogger("csv_processor")
logger.setLevel(logging.INFO)

# ---- File Handler Only ----
file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a")
file_handler.setLevel(logging.INFO)

# Formatter with timestamp
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(file_handler)
