#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile, Author, Book, Library, Librarian

print("=== SETTING UP RBAC TEST DATA ===\n")

# Clear and create fresh data
print("1. Creating test data...")
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create library data
author = Author.objects.create(name="George Orwell")
book1 = Book.objects.create(title="1984", author=author, publication_year=1949)
book2 = Book.objects.create(title="Animal Farm", author=author, publication_year=1945)

library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

Librarian.objects.create(name="John Smith", library=library)
print("   ✅ Library data created")

# Create test users with different roles
print("\n2. Creating test users with roles:")
users_data = [
    ('admin_user', 'adminpass123', 'Admin', 'Admin User'),
    ('librarian_user', 'libpass123', 'Librarian', 'Librarian User'),
    ('member_user', 'memberpass123', 'Member', 'Member User'),
    ('regular_user', 'regularpass123', 'Member', 'Regular User'),
]

for username, password, role, full_name in users_data:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, f'{username}@example.com', password)
        user.first_name = full_name.split()[0]
        user.last_name = full_name.split()[1] if len(full_name.split()) > 1 else ''
        user.save()
        
        # Get or create profile and assign role
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        
        print(f"   ✅ Created {username} with role: {role}")
    else:
        # Update existing user's role
        user = User.objects.get(username=username)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        print(f"   ✅ Updated {username} to role: {role}")

print("\n3. Summary of users created:")
for user in User.objects.all():
    profile = UserProfile.objects.get(user=user)
    print(f"   👤 {user.username:15} | Role: {profile.role:10} | Email: {user.email}")

print("\n=== RBAC TEST DATA SETUP COMPLETE ===")
print("\nTest credentials:")
print("  Admin:      admin_user / adminpass123")
print("  Librarian:  librarian_user / libpass123")
print("  Member:     member_user / memberpass123")
print("\nRole-based URLs:")
print("  Admin:      http://127.0.0.1:8000/admin/dashboard/")
print("  Librarian:  http://127.0.0.1:8000/librarian/dashboard/")
print("  Member:     http://127.0.0.1:8000/member/dashboard/")
