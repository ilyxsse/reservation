
"""
View layer for *rooms*.

Permissions
-----------
* All authenticated users can **list** rooms.
* Only staff users (`is_staff=True`) may **create**, **edit**, or **delete** rooms.
"""
from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RoomForm
from .models import Room


class StaffRequiredMixin(UserPassesTestMixin):
    """Allow access only to staff members (``user.is_staff``)."""

    def test_func(self) -> bool:  # noqa: D401
        return self.request.user.is_staff


class RoomListView(LoginRequiredMixin, ListView):
    """Display all *active* rooms (soft-hiding inactive ones)."""

    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(active=True) if not self.request.user.is_staff else qs


class RoomCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """Create a new room (admin only)."""

    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"
    success_url = reverse_lazy("rooms:list")


class RoomUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """Update an existing room (admin only)."""

    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"
    success_url = reverse_lazy("rooms:list")


class RoomDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    """Soft-delete (or fully delete) a room (admin only)."""

    model = Room
    template_name = "rooms/room_confirm_delete.html"
    success_url = reverse_lazy("rooms:list")

