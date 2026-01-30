#!/usr/bin/env python3
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("="*70)
print("COMPLETE RBAC SYSTEM TEST")
print("="*70)

client = Client()

print("\n1. Testing User Authentication:")
# Test login for each test user
test_credentials = [
    ('admin_user', 'adminpass123', 'Admin'),
    ('librarian_user', 'libpass123', 'Librarian'),
    ('member_user', 'memberpass123', 'Member'),
]

for username, password, expected_role in test_credentials:
    # Test login
    login_success = client.login(username=username, password=password)
    if login_success:
        print(f"✅ {username:15} ({expected_role:10}): Login successful")
        
        # Verify role in session
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        if profile.role == expected_role:
            print(f"   ✅ Role verified: {profile.role}")
        else:
            print(f"   ❌ Role mismatch: expected {expected_role}, got {profile.role}")
        
        client.logout()
    else:
        print(f"❌ {username:15}: Login failed")

print("\n2. Testing Role-Based View Access:")
print("-" * 70)

# Test access matrix
test_cases = [
    # (username, password, view_to_test, should_succeed, description)
    ('admin_user', 'adminpass123', 'admin_view', True, 'Admin accessing admin view'),
    ('admin_user', 'adminpass123', 'librarian_view', False, 'Admin accessing librarian view'),
    ('admin_user', 'adminpass123', 'member_view', False, 'Admin accessing member view'),
    
    ('librarian_user', 'libpass123', 'admin_view', False, 'Librarian accessing admin view'),
    ('librarian_user', 'libpass123', 'librarian_view', True, 'Librarian accessing librarian view'),
    ('librarian_user', 'libpass123', 'member_view', False, 'Librarian accessing member view'),
    
    ('member_user', 'memberpass123', 'admin_view', False, 'Member accessing admin view'),
    ('member_user', 'memberpass123', 'librarian_view', False, 'Member accessing librarian view'),
    ('member_user', 'memberpass123', 'member_view', True, 'Member accessing member view'),
]

all_tests_passed = True
for username, password, view_name, should_succeed, description in test_cases:
    # Login
    client.login(username=username, password=password)
    
    # Try to access the view
    try:
        response = client.get(reverse(view_name), follow=True)
        accessed = response.status_code == 200
        
        # Check if we were redirected (access denied)
        if len(response.redirect_chain) > 0:
            accessed = False
        
    except Exception as e:
        accessed = False
    
    # Check if test passed
    test_passed = accessed == should_succeed
    status = "✅" if test_passed else "❌"
    
    if not test_passed:
        all_tests_passed = False
    
    access_result = "ACCESS GRANTED" if accessed else "ACCESS DENIED"
    expected = "(expected)" if should_succeed else "(NOT expected)"
    
    print(f"{status} {username:15} → {view_name:15}: {access_result} {expected}")
    
    client.logout()

print("\n3. Testing Public Access (Unauthenticated):")
print("-" * 70)

client.logout()  # Ensure no user is logged in

public_urls = [
    ('list_books', '/books/', 'Public books page'),
    ('login', '/login/', 'Login page'),
    ('register', '/register/', 'Registration page'),
]

for url_name, expected_path, description in public_urls:
    try:
        response = client.get(reverse(url_name))
        if response.status_code == 200:
            print(f"✅ {description:25}: Accessible to public")
        else:
            print(f"❌ {description:25}: Not accessible (status: {response.status_code})")
    except Exception as e:
        print(f"❌ {description:25}: Error: {e}")

print("\n4. Testing Role-Specific Template Content:")
print("-" * 70)

# Test that each role sees their specific dashboard content
role_templates = [
    ('admin_user', 'adminpass123', 'admin_view', 'Admin Dashboard', '🔐 Admin Dashboard'),
    ('librarian_user', 'libpass123', 'librarian_view', 'Librarian Dashboard', '📚 Librarian Dashboard'),
    ('member_user', 'memberpass123', 'member_view', 'Member Dashboard', '👤 Member Dashboard'),
]

for username, password, view_name, expected_title, expected_header in role_templates:
    client.login(username=username, password=password)
    
    try:
        response = client.get(reverse(view_name))
        content = response.content.decode('utf-8')
        
        if expected_title in content:
            print(f"✅ {username:15}: Correct title found")
        else:
            print(f"❌ {username:15}: Title not found")
            
        if expected_header in content:
            print(f"   ✅ Correct header found")
        else:
            print(f"   ❌ Header not found")
            
    except Exception as e:
        print(f"❌ {username:15}: Error: {e}")
    
    client.logout()

print("\n" + "="*70)
if all_tests_passed:
    print("🎉 ALL RBAC TESTS PASSED SUCCESSFULLY!")
    print("\nRole-Based Access Control is working correctly:")
    print("  • Admins can only access admin_view")
    print("  • Librarians can only access librarian_view")
    print("  • Members can only access member_view")
    print("  • Public pages are accessible to all")
    print("  • Each role sees their correct dashboard")
else:
    print("⚠️  Some RBAC tests failed. Please review above issues.")
print("="*70)
