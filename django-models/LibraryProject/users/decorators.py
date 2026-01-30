from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from relationship_app.models import UserProfile

def role_required(*roles):
    """
    Decorator for views that checks if the user has one of the specified roles.
    """
    def in_roles(user):
        if not user.is_authenticated:
            return False
        try:
            # Use the new related_name 'user_profile'
            profile = user.user_profile
            return profile.role in roles
        except UserProfile.DoesNotExist:
            return False
    
    return user_passes_test(in_roles, login_url='/accounts/login/')

def admin_required(view_func):
    """Decorator for views that require Admin role"""
    return role_required('Admin')(view_func)

def librarian_required(view_func):
    """Decorator for views that require Librarian role"""
    return role_required('Librarian')(view_func)

def member_required(view_func):
    """Decorator for views that require Member role"""
    return role_required('Member')(view_func)
