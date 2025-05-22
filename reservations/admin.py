
"""
Admin integration for *reservations*.

Useful as a global calendar view and quick-edit interface in addition
to the custom dashboards.  We enable handy filters and search fields so
admins can locate bookings quickly.
"""
from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "date", "hour", "user", "created_at")
    list_filter = ("room", "date")
    search_fields = ("room__name", "user__username")
    ordering = ("-date", "hour")

