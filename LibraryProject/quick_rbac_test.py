#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("=== QUICK RBAC VERIFICATION ===\n")

# Check if test users exist and have correct roles
test_users = ['admin_user', 'librarian_user', 'member_user']

print("Checking test users:")
for username in test_users:
    try:
        user = User.objects.get(username=username)
        print(f"✅ User exists: {username}")
        
        try:
            profile = UserProfile.objects.get(user=user)
            print(f"   Profile exists, role: {profile.role}")
            
            # Check role-specific methods
            if profile.role == 'Admin' and profile.is_admin():
                print("   ✅ is_admin() returns True")
            elif profile.role == 'Librarian' and profile.is_librarian():
                print("   ✅ is_librarian() returns True")
            elif profile.role == 'Member' and profile.is_member():
                print("   ✅ is_member() returns True")
                
        except UserProfile.DoesNotExist:
            print(f"❌ No profile for {username}")
            
    except User.DoesNotExist:
        print(f"❌ User not found: {username}")

print("\n=== VERIFICATION COMPLETE ===")
print("\nTo test in browser:")
print("1. Start server: python3 manage.py runserver")
print("2. Login with:")
print("   - admin_user / adminpass123")
print("   - librarian_user / libpass123")
print("   - member_user / memberpass123")
print("3. Try accessing role-specific dashboards")
