
"""
User model (placeholder).

We can keep Django’s built-in *User* unchanged because the existing
`is_staff` flag is all we need to distinguish Admins from normal users.
No extra profile fields are required right now, but this module is
present so we can extend the model later without a disruptive migration.
"""
from django.contrib.auth.models import User  # re-export for convenience

__all__ = ["User"]

