from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin

def admin_required(view):
    """Verify that the current user is staff (for views)."""
    return user_passes_test(lambda u: u.is_staff)(view)

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is staff (for classes)."""
    def dispatch(self, request, *args, **kwargs):
        """Define dispatcher for the mixin."""
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def superuser_required(view):
    """Verify that the current user is superuser."""
    return user_passes_test(lambda u: u.is_superuser)(view)

class SuperuserRequiredMixin(AccessMixin):
    """Verify that the current user is staff (for classes)."""
    def dispatch(self, request, *args, **kwargs):
        """Define dispatcher for the mixin."""
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
