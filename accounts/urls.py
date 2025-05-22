
"""
URL patterns for the *accounts* app.

- /accounts/login/          → Login form
- /accounts/logout/         → Log out and redirect to login page
- /accounts/signup/         → Optional self-service registration
- /accounts/post-login/     → Decide which dashboard to show
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Optional self-service sign-up
    path("signup/", views.SignupView.as_view(), name="signup"),
    # Post-login router → admin or user dashboard
    path("post-login/", views.PostLoginRedirectView.as_view(), name="post_login"),
]

