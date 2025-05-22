
"""
Development-only settings.

Imported via `manage.py`’s default DJANGO_SETTINGS_MODULE or by explicitly
exporting DJANGO_SETTINGS_MODULE=config.settings.dev.
"""
from .base import *  # noqa: F403,F401  (wild-import is fine for layered settings)

# ---------------------------------------------------------------------------
# Debug flags
# ---------------------------------------------------------------------------

DEBUG = True
ALLOWED_HOSTS = ["*"]  # open during local development

# ---------------------------------------------------------------------------
# Tooling
# ---------------------------------------------------------------------------

# Console email backend so password-reset, etc., simply print to the terminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Optional: install Django-Debug-Toolbar if you like
# INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
# INTERNAL_IPS = ["127.0.0.1"]

