#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("="*70)
print("FINAL RBAC USER SETUP")
print("="*70)

# First, ensure all existing users have profiles
print("\n1. Ensuring all users have UserProfiles...")
users_without_profiles = []
for user in User.objects.all():
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        users_without_profiles.append(user.username)
        # Create profile for missing user
        UserProfile.objects.create(user=user, role='Member')
        print(f"   🔧 Created profile for: {user.username}")

if users_without_profiles:
    print(f"   Created profiles for {len(users_without_profiles)} users")
else:
    print("   ✅ All users already have profiles")

# Now update/create test users with specific roles
print("\n2. Setting up test users with specific roles:")
test_users = [
    ('admin_user', 'adminpass123', 'Admin'),
    ('librarian_user', 'libpass123', 'Librarian'),
    ('member_user', 'memberpass123', 'Member'),
]

for username, password, role in test_users:
    # Create or get user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@example.com',
            'is_active': True
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        action = "Created"
    else:
        action = "Updated"
    
    # Ensure user has the correct password
    if not user.check_password(password):
        user.set_password(password)
        user.save()
    
    # Get or create profile and set role
    profile, profile_created = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    
    profile_action = "created" if profile_created else "updated"
    print(f"   ✅ {action:7} {username:15} → Role: {role:10} (profile {profile_action})")

print("\n3. Current user status:")
print("-" * 70)
print(f"{'Username':15} | {'Role':10} | {'Has Profile':12} | {'Email':25}")
print("-" * 70)

for user in User.objects.all().order_by('username'):
    try:
        profile = UserProfile.objects.get(user=user)
        has_profile = "✅ Yes"
        role = profile.role
    except UserProfile.DoesNotExist:
        has_profile = "❌ No"
        role = "N/A"
    
    print(f"{user.username:15} | {role:10} | {has_profile:12} | {user.email or 'No email':25}")

print("\n" + "="*70)
print("🎉 RBAC USER SETUP COMPLETE!")
print("\nTest credentials:")
print("  👑 Admin:      admin_user      / adminpass123")
print("  📚 Librarian:  librarian_user  / libpass123")
print("  👤 Member:     member_user     / memberpass123")
print("\nTest URLs:")
print("  🔐 Admin Panel:      http://127.0.0.1:8000/admin/dashboard/")
print("  📖 Librarian Panel:  http://127.0.0.1:8000/librarian/dashboard/")
print("  👤 Member Panel:     http://127.0.0.1:8000/member/dashboard/")
print("  📚 All Books:        http://127.0.0.1:8000/books/")
print("="*70)
