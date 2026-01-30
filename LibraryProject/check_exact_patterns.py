#!/usr/bin/env python3
import os

print("=== CHECKING FOR EXACT PATTERNS ===\n")

urls_path = "relationship_app/urls.py"
if os.path.exists(urls_path):
    with open(urls_path, 'r') as f:
        content = f.read()
    
    print("Checking urls.py for EXACT patterns:")
    print("-" * 50)
    
    # The test is looking for these EXACT strings
    exact_patterns = [
        'views.register',
        'LoginView.as_view(template_name="',
        'LogoutView.as_view(template_name="',
    ]
    
    for pattern in exact_patterns:
        if pattern in content:
            print(f"✅ Found: {pattern}")
        else:
            print(f"❌ Missing: {pattern}")
            
            # Show what we actually have
            lines = content.split('\n')
            for line in lines:
                if 'register' in line or 'LoginView' in line or 'LogoutView' in line:
                    print(f"   Instead have: {line.strip()}")
    
    print("\nFull urls.py:")
    print("-" * 50)
    print(content)
    
else:
    print("❌ urls.py not found")
