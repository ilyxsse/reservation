
"""
Database model for a *meeting room*.

Fields
------
name        : Human-readable identifier (unique).
capacity    : Number of people the room can comfortably hold.
location    : Optional description (e.g. “2nd floor, West Wing”).
amenities   : Free-text list (comma-separated) of available equipment.
active      : Toggle to soft-hide retired or out-of-service rooms.

The `__str__` representation is the room’s name so it displays nicely in
admin drop-downs and Django shell sessions.
"""
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=255, blank=True)
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated list of amenities, e.g. Projector, Whiteboard",
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # noqa: D401
        return self.name

