
"""
Base (common) Django settings.

All environment-specific settings files (e.g. dev.py, prod.py) import from
this module and then override as necessary.

Only put values here that are *identical* across every environment.
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent  # project root
load_dotenv(BASE_DIR / ".env", override=False)  # silently ignore if missing

def env(key: str, default=None, cast=str):
    """Small wrapper around os.getenv with type-casting support."""
    val = os.getenv(key, default)
    return cast(val) if val is not None else None

# ---------------------------------------------------------------------------
# Core settings
# ---------------------------------------------------------------------------

SECRET_KEY: str = env("SECRET_KEY", "dev-unsafe-change-me")
DEBUG: bool = bool(int(env("DEBUG", 1)))
ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party (add more as needed)
    "whitenoise.runserver_nostatic",  # static files in prod & dev
    # Project apps
    "accounts",
    "rooms",
    "reservations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # shared layouts & dashboards
        "APP_DIRS": True,                  # app-specific template folders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database — simple SQLite by default; override in prod.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalisation
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Casablanca"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # collected in prod
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key type (matches AppConfig in config/__init__.py)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:post_login"
LOGOUT_REDIRECT_URL = "accounts:login"

