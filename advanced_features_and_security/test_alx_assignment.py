#!/usr/bin/env python
"""
ALX Django Permissions Assignment - Final Test
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

print("="*70)
print("ALX DJANGO PERMISSIONS & GROUPS ASSIGNMENT - FINAL VERIFICATION")
print("="*70)

all_tests_passed = True

# Test 1: Check custom permissions
print("\n1. CUSTOM PERMISSIONS (Step 1):")
print("   Checking Article model permissions...")

try:
    article_ct = ContentType.objects.get(app_label='content', model='article')
    article_perms = Permission.objects.filter(content_type=article_ct)
    
    required_article_perms = [
        ('can_view', 'Can view article'),
        ('can_create', 'Can create article'),
        ('can_edit', 'Can edit article'),
        ('can_delete', 'Can delete article'),
    ]
    
    for codename, name in required_article_perms:
        exists = article_perms.filter(codename=codename).exists()
        if exists:
            print(f"   ✓ {codename} - {name}")
        else:
            print(f"   ✗ MISSING: {codename}")
            all_tests_passed = False
    
    # Check for can_publish (bonus)
    can_publish_exists = article_perms.filter(codename='can_publish').exists()
    if can_publish_exists:
        print(f"   ✓ can_publish - Can publish article (bonus)")
    
except Exception as e:
    print(f"   ✗ Error checking permissions: {e}")
    all_tests_passed = False

# Test 2: Check groups
print("\n2. GROUPS CONFIGURATION (Step 2):")
required_groups = ['Viewers', 'Editors', 'Admins']

for group_name in required_groups:
    try:
        group = Group.objects.get(name=group_name)
        perms_count = group.permissions.count()
        print(f"   ✓ {group_name} group exists with {perms_count} permissions")
        
        # Show permissions for each group
        perms = group.permissions.all()
        perm_names = [p.codename for p in perms]
        if perm_names:
            print(f"     Permissions: {', '.join(perm_names[:5])}")
            if len(perm_names) > 5:
                print(f"     ... and {len(perm_names) - 5} more")
        
    except Group.DoesNotExist:
        print(f"   ✗ {group_name} group NOT FOUND")
        all_tests_passed = False
    except Exception as e:
        print(f"   ✗ Error checking {group_name}: {e}")
        all_tests_passed = False

# Test 3: Check views protection (file check)
print("\n3. VIEWS PROTECTION (Step 3):")
try:
    with open('content/views.py', 'r') as f:
        views_content = f.read()
    
    required_decorators = [
        "@permission_required('content.can_view'",
        "@permission_required('content.can_create'",
        "@permission_required('content.can_edit'",
        "@permission_required('content.can_delete'",
    ]
    
    decorator_count = 0
    for decorator in required_decorators:
        count = views_content.count(decorator)
        if count > 0:
            perm_name = decorator.split("'")[1]
            print(f"   ✓ {perm_name} found ({count} times)")
            decorator_count += count
        else:
            print(f"   ⚠  {decorator.split("'")[1]} not found in views")
    
    if decorator_count >= 4:
        print(f"   ✓ All required permission decorators implemented")
    else:
        print(f"   ⚠  Only {decorator_count}/4 decorators found")
        all_tests_passed = False
    
except FileNotFoundError:
    print("   ✗ content/views.py not found")
    all_tests_passed = False
except Exception as e:
    print(f"   ✗ Error checking views: {e}")
    all_tests_passed = False

# Test 4: Check documentation
print("\n4. DOCUMENTATION (Step 5):")
docs_exist = os.path.exists('PERMISSIONS_SETUP.md')
if docs_exist:
    print("   ✓ PERMISSIONS_SETUP.md documentation exists")
    with open('PERMISSIONS_SETUP.md', 'r') as f:
        doc_content = f.read()
        if 'ALX' in doc_content or 'Assignment' in doc_content:
            print("   ✓ Documentation includes assignment details")
        else:
            print("   ⚠  Documentation may not be assignment-specific")
else:
    print("   ✗ PERMISSIONS_SETUP.md not found")
    all_tests_passed = False

# Test 5: Check file structure
print("\n5. FILE STRUCTURE:")
required_files = [
    'content/models.py',
    'content/views.py',
    'content/urls.py',
    'content/management/commands/setup_groups.py',
]

for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} not found")
        all_tests_passed = False

print("\n" + "="*70)
if all_tests_passed:
    print("✅ ALL ASSIGNMENT REQUIREMENTS MET!")
    print("   Your implementation is complete and ready for testing.")
else:
    print("⚠️  SOME REQUIREMENTS NOT MET")
    print("   Please check the issues above.")
print("="*70)

print("\nNEXT STEPS FOR TESTING:")
print("1. Start server: python manage.py runserver")
print("2. Create superuser (if not done): python manage.py createsuperuser")
print("3. Access admin: http://127.0.0.1:8000/admin/")
print("4. Create test users and assign to groups:")
print("   - viewer@test.com → Viewers group")
print("   - editor@test.com → Editors group")
print("   - admin@test.com → Admins group")
print("5. Test permissions at: http://127.0.0.1:8000/content/")
print("6. Verify each user can only perform actions based on their permissions")
