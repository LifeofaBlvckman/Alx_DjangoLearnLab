#!/usr/bin/env python
"""
ALX Security Assignment Verification Script
"""
import os
import sys
import django

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

from django.conf import settings

print("="*60)
print("ALX Django Security Assignment - Verification")
print("="*60)

requirements = {
    "DEBUG = False": (not settings.DEBUG, "DEBUG must be False for production"),
    "CSRF_COOKIE_SECURE = True": (settings.CSRF_COOKIE_SECURE, "CSRF cookies should be secure"),
    "SESSION_COOKIE_SECURE = True": (settings.SESSION_COOKIE_SECURE, "Session cookies should be secure"),
    "SECURE_BROWSER_XSS_FILTER = True": (settings.SECURE_BROWSER_XSS_FILTER, "XSS filter should be enabled"),
    "X_FRAME_OPTIONS = 'DENY'": (settings.X_FRAME_OPTIONS == 'DENY', "Should deny framing"),
    "SECURE_CONTENT_TYPE_NOSNIFF = True": (settings.SECURE_CONTENT_TYPE_NOSNIFF, "Should prevent MIME sniffing"),
    "CSP Middleware installed": ('csp.middleware.CSPMiddleware' in settings.MIDDLEWARE, "CSP middleware should be installed"),
}

all_passed = True
for req, (check, message) in requirements.items():
    if check:
        print(f"✅ {req}")
    else:
        print(f"❌ {req}")
        print(f"   {message}")
        all_passed = False

print("\n" + "="*60)
if all_passed:
    print("✅ ALL SECURITY REQUIREMENTS MET!")
    print("\nFiles to check:")
    print("1. LibraryProject/settings.py - Security configurations")
    print("2. bookshelf/views.py - Secure view implementations")
    print("3. bookshelf/templates/ - CSRF tokens in forms")
    print("4. SECURITY_DOCUMENTATION.md - Implementation details")
else:
    print("❌ SOME REQUIREMENTS NOT MET")
    print("Please check the errors above.")

print("="*60)

# Check file existence
print("\nChecking required files:")
required_files = [
    'LibraryProject/settings.py',
    'bookshelf/views.py',
    'bookshelf/templates/bookshelf/form_example.html',
    'SECURITY_DOCUMENTATION.md',
    'README.md',
]

for file_path in required_files:
    if os.path.exists(file_path):
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - MISSING")
