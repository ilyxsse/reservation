
"""
Database model for a single *reservation*.

A booking is always one *full hour* long.  We store just the **start hour**
(08 → 17) because the end hour is derivable (+1 h).  Each (room, date, hour)
tuple must be unique—this is enforced via the ``unique_together`` constraint.

Fields
------
room        : FK → Room being booked
user        : FK → User who made the booking
date        : Date of the meeting (YYYY-MM-DD, stored in local TZ)
hour        : Hour-of-day (24-h clock, int 8–17 inclusive; start time)
created_at  : Audit timestamp

Validation
----------
• Hour must be within working hours (08–18)
• No double-booking (enforced by DB constraint + clean())
"""
from __future__ import annotations

import datetime as _dt

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from rooms.models import Room
from accounts.models import User  # re-exported alias


def _default_date() -> _dt.date:
    """Pre-select *today* in forms, in local timezone."""
    return timezone.localdate()


class Reservation(models.Model):
    WORK_START = 8
    WORK_END = 18  # exclusive upper-bound

    HOUR_CHOICES = [(h, f"{h:02d}:00") for h in range(WORK_START, WORK_END)]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reservations")
    date = models.DateField(default=_default_date)
    hour = models.PositiveSmallIntegerField(choices=HOUR_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "date", "hour")
        ordering = ("-date", "hour")

    # ------------------------------------------------------------------ #
    # Business logic helpers                                             #
    # ------------------------------------------------------------------ #
    def clean(self) -> None:
        """
        Extra validation beyond ``unique_together``.

        • Ensure hour is within working-hours bounds.
        • Check for double-booking in Python—useful for friendlier error
          messages before the DB constraint fires.
        """
        if not (self.WORK_START <= self.hour < self.WORK_END):
            raise ValidationError(
                {"hour": "Hour must be between 08:00 and 17:00 inclusive."}
            )

        # Collision check (excluding self when updating)
        collision_qs = (
            Reservation.objects.filter(room=self.room, date=self.date, hour=self.hour)
            .exclude(pk=self.pk)
            .exists()
        )
        if collision_qs:
            raise ValidationError(
                "This room is already booked for the selected date & time."
            )

    # ------------------------------------------------------------------ #
    # Convenience properties                                             #
    # ------------------------------------------------------------------ #
    @property
    def start_time(self) -> _dt.datetime:
        """Return a full datetime (local TZ) representing the booking start."""
        return timezone.make_aware(
            _dt.datetime.combine(self.date, _dt.time(self.hour, 0))
        )

    @property
    def end_time(self) -> _dt.datetime:
        """Return the end datetime—exactly one hour after *start_time*."""
        return self.start_time + _dt.timedelta(hours=1)

    # ------------------------------------------------------------------ #
    # Representation                                                     #
    # ------------------------------------------------------------------ #
    def __str__(self) -> str:  # noqa: D401
        return f"{self.room} on {self.date} at {self.hour:02d}:00"

