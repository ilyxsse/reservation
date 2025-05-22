
"""
Forms for the *reservations* app.

`ReservationForm` wraps the `Reservation` model so users can pick a room,
a date, and an *hour-long* slot (08:00 → 17:00).  We add:

• Bootstrap-compatible widgets
• Validation blocking past dates and double-bookings *before* they hit the DB
"""
from __future__ import annotations

import datetime as _dt

from django import forms
from django.utils import timezone

from .models import Reservation


class ReservationForm(forms.ModelForm):
    """Create a new one-hour booking (all authenticated users)."""

    class Meta:
        model = Reservation
        fields = ["room", "date", "hour"]
        widgets = {
            "room": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    # Prevent picking a date in the past on modern browsers
                    "min": timezone.localdate().isoformat(),
                }
            ),
            "hour": forms.Select(attrs={"class": "form-select"}),
        }

    # ------------------------------------------------------------------ #
    # Extra field-level validation                                       #
    # ------------------------------------------------------------------ #
    def clean_date(self) -> _dt.date:  # noqa: D401
        """Reject dates earlier than today."""
        chosen = self.cleaned_data["date"]
        if chosen < timezone.localdate():
            raise forms.ValidationError("You can only book today or a future date.")
        return chosen

    # ------------------------------------------------------------------ #
    # Cross-field validation (room + date + hour)                        #
    # ------------------------------------------------------------------ #
    def clean(self):  # noqa: D401
        """
        Ensure the selected slot is still free.

        This duplicates model.clean() so users see an inline message rather
        than a generic integrity-error page if two people race to book.
        """
        cleaned = super().clean()
        room = cleaned.get("room")
        date = cleaned.get("date")
        hour = cleaned.get("hour")

        if room and date and hour is not None:
            conflict = (
                Reservation.objects.filter(room=room, date=date, hour=hour)
                .exclude(pk=self.instance.pk)
                .exists()
            )
            if conflict:
                raise forms.ValidationError(
                    "That room is already booked for the selected time."
                )

        return cleaned

