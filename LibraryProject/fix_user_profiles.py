#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("=== FIXING USER PROFILES ===")

# Get all users
users = User.objects.all()
print(f"Found {users.count()} users in database")

# Create UserProfile for any user that doesn't have one
profiles_created = 0
profiles_updated = 0

for user in users:
    try:
        # Try to get existing profile
        profile = UserProfile.objects.get(user=user)
        print(f"   ✅ {user.username:15} already has profile: {profile.role}")
        profiles_updated += 1
    except UserProfile.DoesNotExist:
        # Create new profile with default role
        profile = UserProfile.objects.create(user=user, role='Member')
        print(f"   🔧 {user.username:15} created profile with role: {profile.role}")
        profiles_created += 1

print(f"\nSummary:")
print(f"  Total users: {users.count()}")
print(f"  Profiles created: {profiles_created}")
print(f"  Profiles already existed: {profiles_updated}")

# Verify all users now have profiles
print("\nVerification:")
all_users_have_profiles = True
for user in User.objects.all():
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"   ✅ {user.username:15} -> {profile.role}")
    except UserProfile.DoesNotExist:
        print(f"   ❌ {user.username:15} -> NO PROFILE")
        all_users_have_profiles = False

if all_users_have_profiles:
    print("\n🎉 All users now have UserProfiles!")
else:
    print("\n⚠️  Some users still don't have profiles")
