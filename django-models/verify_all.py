#!/usr/bin/env python3
import os
import sys

print("="*60)
print("FINAL VERIFICATION OF DJANGO VIEWS IMPLEMENTATION")
print("="*60)

all_passed = True

# 1. Check views.py
print("\n1. VERIFYING VIEWS.PY")
print("-"*40)
views_file = "django-models/LibraryProject/relationship_app/views.py"
if os.path.exists(views_file):
    with open(views_file, 'r') as f:
        content = f.read()
        
    checks = [
        ("Function-based view exists", "def list_books" in content),
        ("Class-based view exists", "class LibraryDetailView" in content),
        ("Uses Django's DetailView", "DetailView" in content and "LibraryDetailView(DetailView)" in content),
        ("Model specified", "model = Library" in content),
        ("Template specified", "template_name =" in content),
        ("Context object name", "context_object_name = 'library'" in content),
        ("Optimized query", "prefetch_related('books__author')" in content),
    ]
    
    for check_name, passed in checks:
        if passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
else:
    print("   ❌ views.py not found")
    all_passed = False

# 2. Check urls.py
print("\n2. VERIFYING URLS.PY")
print("-"*40)
urls_file = "django-models/LibraryProject/relationship_app/urls.py"
if os.path.exists(urls_file):
    with open(urls_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("Function-based view URL", "path('books/'" in content and "list_books" in content),
        ("Class-based view URL", "path('library/" in content and "LibraryDetailView.as_view()" in content),
        ("Named URLs", "name='list_books'" in content and "name='library_detail'" in content),
    ]
    
    for check_name, passed in checks:
        if passed:
            print(f"   ✅ {check_name}")
        else:
            print(f"   ❌ {check_name}")
            all_passed = False
else:
    print("   ❌ relationship_app/urls.py not found")
    all_passed = False

# 3. Check templates
print("\n3. VERIFYING TEMPLATES")
print("-"*40)
templates_dir = "django-models/LibraryProject/relationship_app/templates/relationship_app"
list_books_tpl = os.path.join(templates_dir, "list_books.html")
library_detail_tpl = os.path.join(templates_dir, "library_detail.html")

# Check list_books.html
if os.path.exists(list_books_tpl):
    with open(list_books_tpl, 'r') as f:
        content = f.read()
    
    checks = [
        ("Uses books context variable", "{% for book in books %}" in content),
        ("Displays book title", "{{ book.title }}" in content),
        ("Displays author name", "{{ book.author.name }}" in content),
    ]
    
    print("   list_books.html:")
    for check_name, passed in checks:
        if passed:
            print(f"     ✅ {check_name}")
        else:
            print(f"     ❌ {check_name}")
            all_passed = False
else:
    print("   ❌ list_books.html not found")
    all_passed = False

# Check library_detail.html
if os.path.exists(library_detail_tpl):
    with open(library_detail_tpl, 'r') as f:
        content = f.read()
    
    checks = [
        ("Uses library context variable", "{{ library.name }}" in content),
        ("Iterates through books", "{% for book in library.books.all %}" in content),
        ("Displays book details", "{{ book.title }}" in content and "{{ book.author.name }}" in content),
        ("Displays publication year", "{{ book.publication_year }}" in content),
    ]
    
    print("\n   library_detail.html:")
    for check_name, passed in checks:
        if passed:
            print(f"     ✅ {check_name}")
        else:
            print(f"     ❌ {check_name}")
            all_passed = False
else:
    print("   ❌ library_detail.html not found")
    all_passed = False

# 4. Check main URLs
print("\n4. VERIFYING MAIN URL CONFIGURATION")
print("-"*40)
main_urls = "django-models/LibraryProject/LibraryProject/urls.py"
if os.path.exists(main_urls):
    with open(main_urls, 'r') as f:
        content = f.read()
    
    if "include('relationship_app.urls')" in content:
        print("   ✅ relationship_app URLs included in main urls.py")
    else:
        print("   ❌ relationship_app URLs not included in main urls.py")
        all_passed = False
else:
    print("   ❌ main urls.py not found")
    all_passed = False

# 5. Check models for publication_year
print("\n5. VERIFYING MODEL UPDATES")
print("-"*40)
models_file = "django-models/LibraryProject/relationship_app/models.py"
if os.path.exists(models_file):
    with open(models_file, 'r') as f:
        content = f.read()
    
    if "publication_year" in content:
        print("   ✅ Book model has publication_year field")
    else:
        print("   ❌ Book model missing publication_year field")
        all_passed = False
else:
    print("   ❌ models.py not found")
    all_passed = False

print("\n" + "="*60)
if all_passed:
    print("🎉 ALL CHECKS PASSED! Implementation is complete and correct.")
    print("\nYou can now push your code:")
    print("  git add .")
    print("  git commit -m 'Complete Django views implementation'")
    print("  git push origin main")
else:
    print("⚠️  Some checks failed. Please fix the issues above.")
print("="*60)
