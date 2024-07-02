#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
from django.core.management import execute_from_command_line


load_dotenv()

ENVIRONMENT: str = str(os.environ.get("DJANGO_ENV")).lower()
VALUE: str = "config.settings.production"

if ENVIRONMENT == "development":
    VALUE = "config.settings.local"


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", VALUE)
    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == "__main__":
    main()
