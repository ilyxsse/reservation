
"""
URL patterns for the *reservations* app.

All authenticated users can view their own bookings and create new ones.
Admins (`is_staff=True`) additionally see **everyone’s** reservations and
may edit / delete any record.

Routes
------
/reservations/                  → ReservationListView        (name="list")
/reservations/create/           → ReservationCreateView      (name="create")
/reservations/<pk>/edit/        → ReservationUpdateView      (name="update")
/reservations/<pk>/delete/      → ReservationDeleteView      (name="delete")
"""
from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("", views.ReservationListView.as_view(), name="list"),
    path("create/", views.ReservationCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ReservationUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.ReservationDeleteView.as_view(), name="delete"),
]

