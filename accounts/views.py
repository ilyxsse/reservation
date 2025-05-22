
"""
Views for the *accounts* app.

Responsibilities
----------------
1. **SignupView** – optional self-service registration of normal users.
2. **PostLoginRedirectView** – smart router that decides whether to send the
   authenticated user to the *Admin* or *User* dashboard after sign-in.

Note: for e-mail confirmation or stronger password rules, extend these
classes later; the API surface stays nicely isolated.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import SignupForm


class SignupView(FormView):
    """
    Render a sign-up form and create a new (non-staff) user.

    * GET  → blank form
    * POST → validate; create user; log them in; redirect to post-login router
    """

    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("accounts:post_login")

    def form_valid(self, form: SignupForm) -> HttpResponseRedirect:  # type: ignore[override]
        """
        If the form is valid, save the user, authenticate, and log them in.

        We deliberately use the cleaned username/password instead of relying on
        Django’s `create_user()` to ensure we can log the user in immediately.
        """
        user = form.save(commit=True)

        # Authenticate & log the user in so they land on their dashboard directly.
        raw_password = form.cleaned_data["password1"]
        authenticated_user = authenticate(
            self.request, username=user.username, password=raw_password
        )
        if authenticated_user:
            login(self.request, authenticated_user)
            messages.success(self.request, "Account created successfully.")
        else:  # pragma: no cover – should not happen
            messages.warning(self.request, "Signup succeeded but auto-login failed.")

        return super().form_valid(form)


class PostLoginRedirectView(LoginRequiredMixin, View):
    """
    Decide where to send a user **after** a successful login.

    • Staff (``is_staff=True``) → Admin dashboard
    • Normal user → User dashboard
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:  # noqa: D401
        destination = (
            "admin_dashboard" if request.user.is_staff else "user_dashboard"
        )
        return redirect(destination)

