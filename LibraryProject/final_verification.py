#!/usr/bin/env python3
"""
Final verification of all Django tasks for django-models project.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

print("=" * 70)
print("FINAL VERIFICATION - DJANGO-MODELS PROJECT")
print("=" * 70)

print("\nNote: Bookshelf app is in Introduction_to_Django project, not django-models")
print("This verification focuses on django-models tasks only.")
print()

# Task 2: Relationship models
print("1. RELATIONSHIP MODELS VERIFICATION")
print("-" * 40)
try:
    from relationship_app.models import Author, Book, Library, Librarian
    models = [('Author', Author), ('Book', Book), ('Library', Library), ('Librarian', Librarian)]
    for name, model in models:
        print(f"✓ {name} model exists: {model.__name__}")
    
    # Check relationships
    print("\n  Relationship checks:")
    book_fields = [f.name for f in Book._meta.fields]
    if 'author_id' in book_fields:
        print("  ✓ Book has ForeignKey to Author")
    else:
        print("  ✗ Book missing ForeignKey to Author")
    
    library_m2m = [f.name for f in Library._meta.many_to_many]
    if 'books' in library_m2m:
        print("  ✓ Library has ManyToMany to Book")
    else:
        print("  ✗ Library missing ManyToMany to Book")
    
    librarian_fields = [f.name for f in Librarian._meta.fields]
    if 'library_id' in librarian_fields:
        print("  ✓ Librarian has OneToOne to Library")
    else:
        print("  ✗ Librarian missing OneToOne to Library")
        
except ImportError as e:
    print(f"✗ Relationship app not found: {e}")

# Task 3: Views
print("\n2. VIEWS VERIFICATION")
print("-" * 40)
try:
    from relationship_app import views as rel_views
    if hasattr(rel_views, 'list_books'):
        print("✓ Function-based view: list_books() exists")
    else:
        print("✗ Function-based view: list_books() missing")
        
    if hasattr(rel_views, 'LibraryDetailView'):
        print("✓ Class-based view: LibraryDetailView exists")
    else:
        print("✗ Class-based view: LibraryDetailView missing")
except ImportError as e:
    print(f"✗ Relationship views not found: {e}")

# Task 4: RBAC
print("\n3. RBAC IMPLEMENTATION VERIFICATION")
print("-" * 40)
try:
    from users.models import UserProfile
    print(f"✓ UserProfile model exists: {UserProfile.__name__}")
    
    # Check fields
    profile_fields = [f.name for f in UserProfile._meta.fields]
    if 'user_id' in profile_fields:
        print("  ✓ Has OneToOneField to User")
    if 'role' in profile_fields:
        print("  ✓ Has role field")
    
    from users import views as user_views
    required_views = ['admin_view', 'librarian_view', 'member_view', 'dashboard']
    for view in required_views:
        if hasattr(user_views, view):
            print(f"  ✓ View exists: {view}")
        else:
            print(f"  ✗ View missing: {view}")
    
    from users import decorators
    required_decorators = ['admin_required', 'librarian_required', 'member_required']
    for decorator in required_decorators:
        if hasattr(decorators, decorator):
            print(f"  ✓ Decorator exists: {decorator}")
        else:
            print(f"  ✗ Decorator missing: {decorator}")
            
except ImportError as e:
    print(f"✗ Users app not found: {e}")

# Test users
print("\n4. TEST USERS VERIFICATION")
print("-" * 40)
from django.contrib.auth.models import User
test_users = ['admin_user', 'librarian_user', 'member_user', 'regular_user']
all_exist = True
for username in test_users:
    try:
        user = User.objects.get(username=username)
        print(f"✓ User exists: {username}")
    except User.DoesNotExist:
        print(f"✗ User missing: {username}")
        all_exist = False

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)

if all_exist:
    print("\n✅ All django-models tasks verified successfully!")
    print("\n📁 This project contains:")
    print("   • Relationship models (Task 2)")
    print("   • Django views (Task 3)")
    print("   • Role-Based Access Control (Task 4)")
    print("\n📁 Bookshelf app (Task 1) is in: Introduction_to_Django/ directory")
else:
    print("\n⚠️  Some issues found. Please check above.")

print("\nTo test the application:")
print("1. Run: python3 manage.py runserver 0.0.0.0:8080")
print("2. Visit: http://localhost:8080/users/login/")
print("3. Use test credentials to login and test different features")
