from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to check if user has required role
    Usage: @role_required(['Admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'profile'):
                if request.user.profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def check_role(role):
    """Test function for user_passes_test decorator"""
    def test_func(user):
        return hasattr(user, 'profile') and user.profile.role == role
    return test_func

# Pre-defined decorators for each role
admin_required = user_passes_test(check_role('Admin'), login_url='/login/')
librarian_required = user_passes_test(check_role('Librarian'), login_url='/login/')
member_required = user_passes_test(check_role('Member'), login_url='/login/')
