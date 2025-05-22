
#!/usr/bin/env python
"""
Django’s command-line utility for administrative tasks.

We point DJANGO_SETTINGS_MODULE to the default “dev” settings so the project
runs immediately after `python manage.py migrate && python manage.py runserver`
without extra environment variables. In production, an explicit override
(e.g. DJANGO_SETTINGS_MODULE=config.settings.prod) is recommended.
"""
import os
import sys


def main() -> None:
    # Default to the development settings module.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

