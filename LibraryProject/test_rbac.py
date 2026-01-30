#!/usr/bin/env python3
"""
Test script to verify Role-Based Access Control is working correctly.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_rbac_access():
    client = Client()
    
    print("=== Testing Role-Based Access Control ===")
    
    # Test 1: Try to access protected views without login
    print("\n1. Testing access without authentication:")
    views = ['/users/admin/', '/users/librarian/', '/users/member/']
    for view in views:
        response = client.get(view)
        print(f"   {view}: {'Redirects to login ✓' if response.status_code == 302 else f'Wrong status: {response.status_code}'}")
    
    # Test 2: Login as member and test access
    print("\n2. Testing as Member user:")
    client.login(username='member_user', password='member123')
    
    response = client.get('/users/member/')
    print(f"   /users/member/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    response = client.get('/users/librarian/')
    print(f"   /users/librarian/: {'Access denied ✓' if response.status_code == 403 or response.status_code == 302 else f'Wrong: {response.status_code}'}")
    
    response = client.get('/users/admin/')
    print(f"   /users/admin/: {'Access denied ✓' if response.status_code == 403 or response.status_code == 302 else f'Wrong: {response.status_code}'}")
    
    client.logout()
    
    # Test 3: Login as librarian and test access
    print("\n3. Testing as Librarian user:")
    client.login(username='librarian_user', password='librarian123')
    
    response = client.get('/users/librarian/')
    print(f"   /users/librarian/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    response = client.get('/users/member/')
    print(f"   /users/member/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    response = client.get('/users/admin/')
    print(f"   /users/admin/: {'Access denied ✓' if response.status_code == 403 or response.status_code == 302 else f'Wrong: {response.status_code}'}")
    
    client.logout()
    
    # Test 4: Login as admin and test access
    print("\n4. Testing as Admin user:")
    client.login(username='admin_user', password='admin123')
    
    response = client.get('/users/admin/')
    print(f"   /users/admin/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    response = client.get('/users/librarian/')
    print(f"   /users/librarian/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    response = client.get('/users/member/')
    print(f"   /users/member/: {'Access granted ✓' if response.status_code == 200 else f'Denied: {response.status_code}'}")
    
    client.logout()
    
    print("\n=== RBAC Tests Completed ===")

if __name__ == "__main__":
    test_rbac_access()
