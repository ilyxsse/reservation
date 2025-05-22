
"""
Production-ready settings.

These are imported when DJANGO_SETTINGS_MODULE=config.settings.prod.
Only overrides and additions that differ from base.py belong here.
"""
from .base import *  # noqa: F401,F403  (import everything from base)

# ---------------------------------------------------------------------------
# Security & performance
# ---------------------------------------------------------------------------

DEBUG = False

# 💡 Populate ALLOWED_HOSTS via environment variable in your deployment stack
#    e.g. `ALLOWED_HOSTS=www.agency-example.com,agency-example.com`
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host]  # noqa: F405

# Enforce HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# HSTS (adjust max_age once you’re confident)
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# Override SQLite with Postgres if DATABASE_URL is provided — simple pattern.
import dj_database_url  # type: ignore

if db_url := os.getenv("DATABASE_URL"):  # noqa: F405
    DATABASES["default"] = dj_database_url.parse(  # noqa: F405
        db_url, conn_max_age=600, ssl_require=True
    )

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
# Configure a real SMTP backend in the environment for password resets.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
# collectstatic places files into STATIC_ROOT; WhiteNoise serves them.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

