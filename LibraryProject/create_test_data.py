#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

print("Creating test data for relationship_app...")

# Check if data already exists
if Book.objects.exists() or Author.objects.exists() or Library.objects.exists():
    print("Data already exists! Skipping creation.")
    print("Current counts:")
    print(f"  Authors: {Author.objects.count()}")
    print(f"  Books: {Book.objects.count()}")
    print(f"  Libraries: {Library.objects.count()}")
    print("\nIf you want fresh data, run:")
    print("  python3 manage.py shell")
    print("  Then manually delete data if needed")
    sys.exit(0)

# Create authors
try:
    authors = [
        Author.objects.create(name="J.K. Rowling"),
        Author.objects.create(name="George Orwell"),
        Author.objects.create(name="Harper Lee"),
        Author.objects.create(name="F. Scott Fitzgerald"),
        Author.objects.create(name="Jane Austen"),
    ]
    print(f"✓ Created {len(authors)} authors")
except Exception as e:
    print(f"✗ Error creating authors: {e}")
    sys.exit(1)

# Create books
try:
    books = [
        Book.objects.create(title="Harry Potter", author=authors[0], publication_year=1997),
        Book.objects.create(title="1984", author=authors[1], publication_year=1949),
        Book.objects.create(title="To Kill a Mockingbird", author=authors[2], publication_year=1960),
        Book.objects.create(title="The Great Gatsby", author=authors[3], publication_year=1925),
        Book.objects.create(title="Pride and Prejudice", author=authors[4], publication_year=1813),
        Book.objects.create(title="Animal Farm", author=authors[1], publication_year=1945),
        Book.objects.create(title="The Casual Vacancy", author=authors[0], publication_year=2012),
    ]
    print(f"✓ Created {len(books)} books")
except Exception as e:
    print(f"✗ Error creating books: {e}")
    sys.exit(1)

# Create libraries
try:
    libraries = [
        Library.objects.create(name="City Central Library"),
        Library.objects.create(name="University Library"),
        Library.objects.create(name="Community Library"),
    ]
    print(f"✓ Created {len(libraries)} libraries")
except Exception as e:
    print(f"✗ Error creating libraries: {e}")
    sys.exit(1)

# Add books to libraries
try:
    libraries[0].books.add(books[0], books[1], books[2], books[3])
    libraries[1].books.add(books[0], books[2], books[4], books[6])
    libraries[2].books.add(books[1], books[3], books[5])
    print("✓ Added books to libraries")
except Exception as e:
    print(f"✗ Error adding books to libraries: {e}")

# Create librarians
try:
    Librarian.objects.create(name="Alice Johnson", library=libraries[0])
    Librarian.objects.create(name="Bob Smith", library=libraries[1])
    Librarian.objects.create(name="Carol Davis", library=libraries[2])
    print("✓ Created librarians")
except Exception as e:
    print(f"✗ Error creating librarians: {e}")

# Print summary
print("\n" + "="*50)
print("TEST DATA CREATED SUCCESSFULLY!")
print("="*50)
print(f"\n📊 Summary:")
print(f"  Authors: {Author.objects.count()}")
print(f"  Books: {Book.objects.count()}")
print(f"  Libraries: {Library.objects.count()}")
print(f"  Librarians: {Librarian.objects.count()}")

print("\n📚 Library details:")
for lib in Library.objects.all():
    book_count = lib.books.count()
    book_titles = ", ".join([b.title[:15] + "..." if len(b.title) > 15 else b.title for b in lib.books.all()[:2]])
    if book_count > 2:
        book_titles += f" and {book_count - 2} more"
    print(f"  • {lib.name}: {book_count} books")

print("\n🌐 URLs to test:")
print("  1. Function-based view: http://127.0.0.1:8000/books/")
print("  2. Class-based views:")
print("     • http://127.0.0.1:8000/library/1/ (City Central Library)")
print("     • http://127.0.0.1:8000/library/2/ (University Library)")
print("     • http://127.0.0.1:8000/library/3/ (Community Library)")
print("\n🚀 Start server: python3 manage.py runserver")
