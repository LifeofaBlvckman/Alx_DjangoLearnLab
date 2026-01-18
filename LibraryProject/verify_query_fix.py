#!/usr/bin/env python3
import os

print("=== VERIFYING query_samples.py ===")

file_path = "relationship_app/query_samples.py"
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check for the exact required query
    if "Library.objects.get(name=library_name)" in content:
        print("✅ SUCCESS: Contains 'Library.objects.get(name=library_name)'")
        
        # Show context
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "Library.objects.get(name=library_name)" in line:
                print(f"\nFound at line {i+1}:")
                # Show a few lines before and after
                start = max(0, i-2)
                end = min(len(lines), i+3)
                for j in range(start, end):
                    prefix = ">>> " if j == i else "    "
                    print(f"{prefix}{lines[j]}")
    else:
        print("❌ FAIL: Still missing 'Library.objects.get(name=library_name)'")
        
    # Also check if the script is executable
    if os.access(file_path, os.X_OK):
        print("✅ File is executable")
    else:
        print("⚠️  File is not executable")
        
else:
    print(f"❌ File not found: {file_path}")
