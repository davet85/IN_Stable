# utils/logger.py

import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Generate dynamic log file name
log_file = os.path.join(LOG_DIR, f"introspect_{datetime.now().strftime('%Y-%m-%d')}.log")

# Logger setup
logger = logging.getLogger("IntrospectLogger")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Attach handlers only once
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Exported functions
def log_info(msg: str):
    logger.info(msg)

def log_error(msg: str):
    logger.error(msg)
