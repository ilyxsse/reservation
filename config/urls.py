
"""
Root URL-dispatcher.

Paths
-----
/admin/                 → Django-admin (superusers only)
/accounts/              → Authentication screens
/rooms/                 → Meeting-room CRUD
/reservations/          → Booking management
/dashboard/admin/       → Staff dashboard  (name="admin_dashboard")
/dashboard/             → User dashboard   (name="user_dashboard")
/                       → Post-login router → correct dashboard
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # Django admin site
    path("admin/", admin.site.urls),
    # Auth & profile
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    # Domain apps
    path("rooms/", include(("rooms.urls", "rooms"), namespace="rooms")),
    path(
        "reservations/",
        include(("reservations.urls", "reservations"), namespace="reservations"),
    ),
    # Dashboards (protected by @login_required)
    path(
        "dashboard/admin/",
        login_required(
            TemplateView.as_view(template_name="dashboards/admin_dashboard.html")
        ),
        name="admin_dashboard",
    ),
    path(
        "dashboard/",
        login_required(
            TemplateView.as_view(template_name="dashboards/user_dashboard.html")
        ),
        name="user_dashboard",
    ),
    # Root → decide which dashboard fits the logged-in user
    path("", RedirectView.as_view(pattern_name="accounts:post_login"), name="root"),
]

