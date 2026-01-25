#!/usr/bin/env python3
"""
Script to create test users with different roles for RBAC testing.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

def create_test_users():
    """Create test users with different roles"""
    
    # Clear existing test users (but keep superusers)
    test_users = ['admin_user', 'librarian_user', 'member_user', 'regular_user']
    User.objects.filter(username__in=test_users).delete()
    
    # Create Admin user
    admin_user = User.objects.create_user(
        username='admin_user',
        email='admin@example.com',
        password='admin123'
    )
    admin_profile = admin_user.profile
    admin_profile.role = 'Admin'
    admin_profile.save()
    print(f"✓ Created Admin user: {admin_user.username} (password: admin123)")
    
    # Create Librarian user
    librarian_user = User.objects.create_user(
        username='librarian_user',
        email='librarian@example.com',
        password='librarian123'
    )
    librarian_profile = librarian_user.profile
    librarian_profile.role = 'Librarian'
    librarian_profile.save()
    print(f"✓ Created Librarian user: {librarian_user.username} (password: librarian123)")
    
    # Create Member user
    member_user = User.objects.create_user(
        username='member_user',
        email='member@example.com',
        password='member123'
    )
    member_profile = member_user.profile
    member_profile.role = 'Member'
    member_profile.save()
    print(f"✓ Created Member user: {member_user.username} (password: member123)")
    
    # Create regular user (no specific role - will default to Member)
    regular_user = User.objects.create_user(
        username='regular_user',
        email='regular@example.com',
        password='regular123'
    )
    print(f"✓ Created Regular user: {regular_user.username} (password: regular123)")
    
    print("\n=== Test Users Created ===")
    print("Login URLs (when server is running):")
    print("1. Admin:      http://localhost:8000/users/admin/")
    print("2. Librarian:  http://localhost:8000/users/librarian/")
    print("3. Member:     http://localhost:8000/users/member/")
    print("4. Dashboard:  http://localhost:8000/users/dashboard/")
    print("\nNote: You need to be logged in to access these pages.")

if __name__ == "__main__":
    create_test_users()
