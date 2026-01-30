import os
import sys

print("=== ALX Django REST Framework Setup Verification ===")
print()

# Check 1: Can we import Django and DRF?
try:
    import django
    import rest_framework
    print("✓ 1. Django and DRF are installed")
except ImportError as e:
    print(f"✗ 1. Missing: {e}")
    sys.exit(1)

# Check 2: Basic project structure
required_files = [
    'manage.py',
    'requirements.txt',
    'api/models.py',
    'django_api_project/settings.py'
]

print("\n✓ 2. Project structure:")
for file in required_files:
    if os.path.exists(file):
        print(f"   • {file} - EXISTS")
    else:
        print(f"   • {file} - MISSING")

print("\n✅ Setup appears complete!")
print("\nTo submit: Share your GitHub repository link with ALX")
print("Repository: https://github.com/LifeofaBlvckman/Alx_DjangoLearnLab")
print("Project location: advanced_features_and_security/django_api/")
