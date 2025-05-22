
"""
URL patterns for the *rooms* app.

Everyone (logged-in) can see the list of rooms.
Only **staff** (``is_staff=True``) may add, edit, or delete rooms.

Routes
------
/rooms/                     → RoomListView                 (name="list")
/rooms/create/              → RoomCreateView               (name="create")   [admin]
/rooms/<pk>/edit/           → RoomUpdateView               (name="update")   [admin]
/rooms/<pk>/delete/         → RoomDeleteView               (name="delete")   [admin]
"""
from django.urls import path

from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomListView.as_view(), name="list"),
    path("create/", views.RoomCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.RoomUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.RoomDeleteView.as_view(), name="delete"),
]

