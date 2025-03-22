# src/config.py

from dynaconf import Dynaconf
import logging

# Load settings from settings.toml
settings = Dynaconf(
    settings_files=["settings.toml"],
    environments=True,
    load_dotenv=True,
)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("✅ Settings loaded successfully")
