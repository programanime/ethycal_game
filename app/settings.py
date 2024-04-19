import logging
import os
from typing import Final

ENVIRONMENT: Final = os.getenv("GAME_ENV", "").lower() or "dev"
LOGGING_LEVEL: Final = logging.DEBUG if ENVIRONMENT != "production" else logging.INFO

# Application common
SECRET_KEY: Final = os.getenv("GAME_SESSION_SECRET")
SESSION_COOKIE_NAME: Final = os.getenv("SESSION_COOKIE_NAME")
SESSION_COOKIE_SECURE: Final = os.getenv("SESSION_COOKIE_SECURE") == "True"
SESSION_COOKIE_DOMAIN: Final = os.getenv("SESSION_COOKIE_DOMAIN")
TESTING: Final = os.getenv("TESTING", "0") == "1"

# Database
DB_URI: Final = "sqlite:///game.db"

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
]
