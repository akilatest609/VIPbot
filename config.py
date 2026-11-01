# config.py
import os
import logging

# Securely load credentials from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID_RAW = os.environ.get("ADMIN_ID")
ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW else None

DB_PATH = "bot.db"
GROUP_SIZE = 10                  # Telegram max per media group
GROUP_DELAY_SECONDS = 5.5          # delay between groups
ITEM_RETRY_DELAY_SECONDS = 3.0     # increased retry delay for larger files
MAX_ITEM_RETRIES = 3
COUNTER_DEBOUNCE_SECONDS = 1.2     # batches rapid forwards into fewer edits
PENDING_SESSION_TTL_SECONDS = 3600  # abandoned /get_link sessions auto-expire

# Custom timeouts for handling larger video files smoothly (up to 50MB Bot API limit)
READ_TIMEOUT = 120.0
WRITE_TIMEOUT = 120.0
CONNECT_TIMEOUT = 30.0
POOL_TIMEOUT = 30.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("videobot")

DURATION_OPTIONS = [
    ("1 min", 60),
    ("5 min", 300),
    ("1 hr", 3600),
    ("1 day", 86400),
]