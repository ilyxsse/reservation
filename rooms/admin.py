
"""
Admin integration for *rooms*.

Registers the Room model so site administrators can manage rooms through
Django-admin (useful for quick data entry or emergency edits even though a
dedicated UI exists).

The list view shows the most important columns and enables filtering
and search for convenience.
"""
from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "location", "active")
    list_filter = ("active",)
    search_fields = ("name", "location", "amenities")
    ordering = ("name",)

