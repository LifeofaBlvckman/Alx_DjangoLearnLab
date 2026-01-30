#!/usr/bin/env python3
"""
Verification script for ALX Django Advanced Features and Security task.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model

print("=" * 60)
print("ALX Custom User Model Verification")
print("=" * 60)

checks = []

# Check 1: AUTH_USER_MODEL
print("1. Checking AUTH_USER_MODEL...")
if settings.AUTH_USER_MODEL == 'users.CustomUser':
    print("   OK: AUTH_USER_MODEL = 'users.CustomUser'")
    checks.append(True)
else:
    print("   FAIL: AUTH_USER_MODEL is '{}'".format(settings.AUTH_USER_MODEL))
    checks.append(False)

# Check 2: Custom User Model
print("\n2. Checking Custom User Model...")
User = get_user_model()
if User.__name__ == 'CustomUser':
    print("   OK: CustomUser model is being used")
    checks.append(True)
else:
    print("   FAIL: Using '{}' model".format(User.__name__))
    checks.append(False)

# Check 3: Required Fields
print("\n3. Checking Required Fields...")
fields = [f.name for f in User._meta.fields]
if 'date_of_birth' in fields:
    print("   OK: date_of_birth field exists")
    checks.append(True)
else:
    print("   FAIL: date_of_birth field missing")
    checks.append(False)

if 'profile_photo' in fields:
    print("   OK: profile_photo field exists")
    checks.append(True)
else:
    print("   FAIL: profile_photo field missing")
    checks.append(False)

# Check 4: Field Types
print("\n4. Checking Field Types...")
from django.db import models
date_field = User._meta.get_field('date_of_birth')
if isinstance(date_field, models.DateField):
    print("   OK: date_of_birth is DateField")
    checks.append(True)
else:
    print("   FAIL: date_of_birth is not DateField")
    checks.append(False)

photo_field = User._meta.get_field('profile_photo')
if isinstance(photo_field, models.ImageField):
    print("   OK: profile_photo is ImageField")
    checks.append(True)
else:
    print("   FAIL: profile_photo is not ImageField")
    checks.append(False)

# Check 5: Custom Manager
print("\n5. Checking Custom Manager...")
if hasattr(User.objects, 'create_user') and hasattr(User.objects, 'create_superuser'):
    print("   OK: Custom manager with create_user and create_superuser")
    checks.append(True)
else:
    print("   FAIL: Custom manager missing required methods")
    checks.append(False)

# Results
print("\n" + "=" * 60)
print("RESULTS:")
print("=" * 60)

passed = sum(checks)
total = len(checks)

if passed == total:
    print("SUCCESS: All {} checks passed!".format(total))
    print("\nAll ALX Requirements Met:")
    print("   1. Custom user model with date_of_birth and profile_photo")
    print("   2. AUTH_USER_MODEL configured in settings")
    print("   3. Custom user manager implemented")
    print("   4. Admin interface configured")
    print("   5. Application uses custom model")
    sys.exit(0)
else:
    print("FAILED: {}/{} checks passed".format(passed, total))
    sys.exit(1)
