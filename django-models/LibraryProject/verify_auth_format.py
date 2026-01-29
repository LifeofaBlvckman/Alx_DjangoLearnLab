#!/usr/bin/env python3
import os

print("=== VERIFYING AUTHENTICATION VIEW FORMAT ===\n")

# Check urls.py
print("1. Checking urls.py for exact patterns:")
urls_path = "relationship_app/urls.py"
if os.path.exists(urls_path):
    with open(urls_path, 'r') as f:
        content = f.read()
    
    required_patterns = [
        "views.register",
        'CustomLoginView.as_view(template_name="relationship_app/login.html")',
        'CustomLogoutView.as_view(template_name="relationship_app/logout.html")',
        "name='register'",
        "name='login'",
        "name='logout'",
    ]
    
    for pattern in required_patterns:
        if pattern in content:
            print(f"   ✅ Contains: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
    
    print("\nFull urls.py content:")
    print("-" * 50)
    print(content)
else:
    print("❌ urls.py not found")

# Check views.py
print("\n2. Checking views.py for required imports:")
views_path = "relationship_app/views.py"
if os.path.exists(views_path):
    with open(views_path, 'r') as f:
        content = f.read()
    
    required_imports = [
        "from django.contrib.auth.views import LoginView, LogoutView",
        "class CustomLoginView(LoginView):",
        "class CustomLogoutView(LogoutView):",
        "def register(request):",
    ]
    
    for pattern in required_imports:
        if pattern in content:
            print(f"   ✅ Contains: {pattern}")
        else:
            print(f"   ❌ Missing: {pattern}")
else:
    print("❌ views.py not found")

print("\n" + "="*60)
print("If all checks pass, update and push your changes.")
print("="*60)
