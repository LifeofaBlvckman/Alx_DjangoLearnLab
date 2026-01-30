from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, librarian_required, member_required

@admin_required
def admin_view(request):
    """View accessible only to users with Admin role"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
    }
    return render(request, 'users/admin_view.html', context)

@librarian_required
def librarian_view(request):
    """View accessible only to users with Librarian role"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
    }
    return render(request, 'users/librarian_view.html', context)

@member_required
def member_view(request):
    """View accessible only to users with Member role"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
    }
    return render(request, 'users/member_view.html', context)

# Optional: Dashboard view that shows different content based on role
@login_required
def dashboard(request):
    """Dashboard view that adapts based on user role"""
    context = {
        'user': request.user,
        'role': request.user.profile.role,
    }
    return render(request, 'users/dashboard.html', context)
