#!/usr/bin/python3
import os

print("=== ALX Checker Requirements ===")
print()

# 1. Check README.md
readme_path = "LibraryProject/README.md"
if os.path.exists(readme_path):
    print(f"✅ README.md: FOUND at {readme_path}")
else:
    print(f"❌ README.md: MISSING at {readme_path}")

# 2. Check manage.py  
manage_path = "LibraryProject/manage.py"
if os.path.exists(manage_path):
    print(f"✅ manage.py: FOUND at {manage_path}")
else:
    print(f"❌ manage.py: MISSING at {manage_path}")

# 3. Check settings.py
settings_path = "LibraryProject/LibraryProject/settings.py"
if os.path.exists(settings_path):
    print(f"✅ settings.py: FOUND at {settings_path}")
else:
    print(f"❌ settings.py: MISSING at {settings_path}")

print()
print("=== Your Structure ===")
os.system("find LibraryProject -type f -name '*.md' -o -name '*.py' | grep -E '(README|manage|settings)' | sort")
