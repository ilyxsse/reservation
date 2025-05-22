
"""
Django project package initialiser.

Keeping this file minimal—only the default auto-field override goes here.
"""
from pathlib import Path

# Automatically use BigAutoField for primary keys, unless overridden.
from django.apps import AppConfig


class DefaultPrimaryKeyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "config"


__all__ = ["Path"]
