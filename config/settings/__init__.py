import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT : str = str(os.environ.get("DJANGO_ENV")).lower()
VALUE : str = "config.settings.production"

if ENVIRONMENT == "development":
    VALUE = "config.settings.local"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", VALUE)
