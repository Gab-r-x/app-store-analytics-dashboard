from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="SCRAPER",
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
)

# Configurations are now accessed using settings.<VAR_NAME>
