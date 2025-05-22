
"""
Forms for the *rooms* app.

`RoomForm` is a thin `ModelForm` wrapper that adds Bootstrap-friendly
widgets so the generated `<input>` elements pick up styling automatically.
"""
from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    """Create / update a meeting room (admin only)."""

    class Meta:
        model = Room
        fields = ["name", "capacity", "location", "amenities", "active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "amenities": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Projector, Whiteboard"}
            ),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

