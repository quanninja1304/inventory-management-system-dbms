import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file (if it exists)
# This allows you to override settings without changing code
load_dotenv()

# Database configuration
# Format: Get from environment variable if exists, otherwise use default value
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # Empty default password
DB_NAME = os.getenv("DB_NAME", "inventory_db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))  # Default MySQL port

# Application settings
APP_NAME = os.getenv("APP_NAME", "Inventory Management System")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DEBUG = os.getenv("APP_DEBUG", "False").lower() == "true"  # Convert string to boolean

# Logging configuration
LOG_FILE = os.getenv("LOG_FILE", "inventory_system.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")

# Convert string log level to logging constant
def get_log_level(level_name):
    """Convert string log level to logging module constant"""
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return levels.get(level_name.upper(), logging.INFO)

LOG_LEVEL_INT = get_log_level(LOG_LEVEL)

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Feature flags - useful for turning features on/off
ENABLE_BACKUPS = os.getenv("ENABLE_BACKUPS", "True").lower() == "true"
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "False").lower() == "true"

# Security settings
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", "60"))
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))

# Define a function to configure logging
def configure_logging():
    """Configure logging based on settings in this file"""
    logging.basicConfig(
        filename=LOG_FILE,
        level=LOG_LEVEL_INT,
        format=LOG_FORMAT
    )
    
    # Add a stream handler if in debug mode
    if APP_DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL_INT)
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)
        logging.getLogger('').addHandler(console_handler)