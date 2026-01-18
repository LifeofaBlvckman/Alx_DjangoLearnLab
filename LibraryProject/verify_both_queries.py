#!/usr/bin/env python3
import os

print("=== VERIFYING BOTH REQUIRED QUERIES ===")

file_path = "relationship_app/query_samples.py"
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    print("1. Checking for 'Author.objects.get(name=author_name)':")
    if "Author.objects.get(name=author_name)" in content:
        print("   ✅ FOUND: Author.objects.get(name=author_name)")
        # Show context
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "Author.objects.get(name=author_name)" in line:
                print(f"\n   Context (line {i+1}):")
                start = max(0, i-1)
                end = min(len(lines), i+2)
                for j in range(start, end):
                    print(f"   {j+1:3}: {lines[j]}")
    else:
        print("   ❌ NOT FOUND: Author.objects.get(name=author_name)")
    
    print("\n2. Checking for 'objects.filter(author=author)':")
    if "objects.filter(author=author)" in content:
        print("   ✅ FOUND: objects.filter(author=author)")
        # Show context
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "objects.filter(author=author)" in line:
                print(f"\n   Context (line {i+1}):")
                start = max(0, i-1)
                end = min(len(lines), i+2)
                for j in range(start, end):
                    print(f"   {j+1:3}: {lines[j]}")
    else:
        print("   ❌ NOT FOUND: objects.filter(author=author)")
    
    print("\n3. Checking for 'Library.objects.get(name=library_name)' (previous requirement):")
    if "Library.objects.get(name=library_name)" in content:
        print("   ✅ FOUND: Library.objects.get(name=library_name)")
    else:
        print("   ❌ NOT FOUND: Library.objects.get(name=library_name)")
    
    print("\n" + "="*60)
    print("SUMMARY:")
    queries_found = 0
    if "Author.objects.get(name=author_name)" in content:
        queries_found += 1
    if "objects.filter(author=author)" in content:
        queries_found += 1
    if "Library.objects.get(name=library_name)" in content:
        queries_found += 1
    
    print(f"Found {queries_found}/3 required queries")
    if queries_found == 3:
        print("🎉 ALL QUERIES FOUND!")
    else:
        print("⚠️  Some queries missing")
    print("="*60)
    
else:
    print(f"❌ File not found: {file_path}")
