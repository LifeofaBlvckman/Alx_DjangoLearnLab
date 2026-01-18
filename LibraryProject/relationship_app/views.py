from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required, admin_required, librarian_required, member_required

# Using custom decorator
@role_required(['Admin'])
def admin_view(request):
    """View accessible only to Admin users"""
    context = {
        'title': 'Admin Dashboard',
        'role': 'Admin',
        'username': request.user.username,
    }
    return render(request, 'admin_view.html', context)

# Using predefined decorators
@librarian_required
def librarian_view(request):
    """View accessible only to Librarian users"""
    context = {
        'title': 'Librarian Dashboard',
        'role': 'Librarian',
        'username': request.user.username,
    }
    return render(request, 'librarian_view.html', context)

@member_required
def member_view(request):
    """View accessible only to Member users"""
    context = {
        'title': 'Member Dashboard',
        'role': 'Member',
        'username': request.user.username,
    }
    return render(request, 'member_view.html', context)

@login_required
def dashboard(request):
    """Redirect users to their role-specific dashboard"""
    if hasattr(request.user, 'profile'):
        role = request.user.profile.role
        
        if role == 'Admin':
            return admin_view(request)
        elif role == 'Librarian':
            return librarian_view(request)
        elif role == 'Member':
            return member_view(request)
    
    # Default fallback
    return render(request, 'dashboard.html', {'user': request.user})

def home(request):
    """Home page view"""
    return render(request, 'home.html')
