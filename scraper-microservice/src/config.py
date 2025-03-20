import os
import logging
from pathlib import Path
from dynaconf import Dynaconf

# Define BASE_DIR correctly, ensuring it works in Docker and local environments
BASE_DIR = Path(__file__).resolve().parent.parent  # Root directory of the project

settings = Dynaconf(
    envvar_prefix="SCRAPER",
    settings_files=[BASE_DIR / "settings.toml", BASE_DIR / ".secrets.toml"],
    environments=True,
    load_dotenv=True,
)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info(f"✅ Loaded settings: {settings.to_dict()}")
