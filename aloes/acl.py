from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

def admin_required(view):
    """Verify that the current user is staff (for views)."""
    return user_passes_test(lambda u: u.is_staff)(view)

class AdminRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is staff (for classes)."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff

def superuser_required(view):
    """Verify that the current user is superuser."""
    return user_passes_test(lambda u: u.is_superuser)(view)

class SuperuserRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is staff (for classes)."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_superuser
