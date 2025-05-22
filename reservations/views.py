
"""
View layer for *reservations*.

Permissions
-----------
* Any authenticated user may **list** their own bookings and create new ones.
* Staff users (`is_staff=True`) see **all** bookings and may edit / delete
  any record.
* Normal users may edit / delete **their own** reservations only.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ReservationForm
from .models import Reservation


# --------------------------------------------------------------------------- #
# Permission helpers                                                          #
# --------------------------------------------------------------------------- #
class StaffOrOwnerMixin(UserPassesTestMixin):
    """
    Allow access if the current user is *staff* **or** is the owner
    of the reservation in question.
    """

    def test_func(self):  # noqa: D401
        obj: Reservation = self.get_object()  # type: ignore[assignment]
        return self.request.user.is_staff or obj.user == self.request.user

    def handle_no_permission(self):  # noqa: D401
        """Raise 404 to avoid leaking the existence of objects."""
        raise Http404


# --------------------------------------------------------------------------- #
# List / create views                                                         #
# --------------------------------------------------------------------------- #
class ReservationListView(LoginRequiredMixin, ListView):
    """
    Show upcoming & past reservations.

    • Staff → see *all* bookings
    • Normal → see *their own* bookings
    """

    model = Reservation
    template_name = "reservations/reservation_list.html"
    context_object_name = "reservations"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        # Show nearest dates first
        return qs.order_by("-date", "-hour")


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """Create a new reservation for the current user."""

    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservations:list")

    def form_valid(self, form):
        # Attach the logged-in user
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Reservation created successfully.")
        return response


# --------------------------------------------------------------------------- #
# Update / delete                                                             #
# --------------------------------------------------------------------------- #
class ReservationUpdateView(LoginRequiredMixin, StaffOrOwnerMixin, UpdateView):
    """Edit an existing reservation (owner or staff)."""

    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("reservations:list")

    def form_valid(self, form):
        messages.success(self.request, "Reservation updated successfully.")
        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, StaffOrOwnerMixin, DeleteView):
    """Remove a reservation."""

    model = Reservation
    template_name = "reservations/reservation_confirm_delete.html"
    success_url = reverse_lazy("reservations:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Reservation deleted.")
        return super().delete(request, *args, **kwargs)

