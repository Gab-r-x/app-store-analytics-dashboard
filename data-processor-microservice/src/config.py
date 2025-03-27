from pathlib import Path
from dynaconf import Dynaconf
import logging
import os

BASE_DIR = Path(__file__).resolve().parent.parent

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=[BASE_DIR / "settings.toml", BASE_DIR / ".secrets.toml"],
    environments=True,
    load_dotenv=True,
)

for key in list(settings.keys()):
    if settings.get(key) == "@env":
        env_value = os.environ.get(key)
        if env_value:
            settings.set(key, env_value)
        else:
            logging.warning(f"⚠️ ENV variable '{key}' not set in environment!")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info(f"✅ Loaded settings: {settings.to_dict()}")
