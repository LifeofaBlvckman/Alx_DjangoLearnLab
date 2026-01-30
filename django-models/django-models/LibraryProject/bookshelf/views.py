from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User

# Helper functions for role checks
def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'profile') and user.profile.role == 'Member'

# Role-based views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html', {
        'user': request.user,
        'role': request.user.profile.role
    })

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html', {
        'user': request.user,
        'role': request.user.profile.role
    })

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html', {
        'user': request.user,
        'role': request.user.profile.role
    })

# Utility view to create test users
def create_test_users(request):
    roles = ['Admin', 'Librarian', 'Member']
    
    for role in roles:
        username = f"test_{role.lower()}"
        email = f"{username}@example.com"
        
        # Create user if doesn't exist
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        
        if created:
            user.set_password('password123')
            user.save()
            user.profile.role = role
            user.profile.save()
    
    # Redirect to admin page or login
    return redirect('admin')
