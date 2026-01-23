#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data
Librarian.objects.all().delete()
Library.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()

# Create authors
author1 = Author.objects.create(name="George Orwell")
author2 = Author.objects.create(name="J.K. Rowling")
author3 = Author.objects.create(name="Harper Lee")
author4 = Author.objects.create(name="F. Scott Fitzgerald")

# Create books
books_data = [
    ("1984", author1),
    ("Animal Farm", author1),
    ("Harry Potter and the Sorcerer's Stone", author2),
    ("Harry Potter and the Chamber of Secrets", author2),
    ("To Kill a Mockingbird", author3),
    ("Go Set a Watchman", author3),
    ("The Great Gatsby", author4),
    ("Tender Is the Night", author4),
]

books = []
for title, author in books_data:
    book = Book.objects.create(title=title, author=author)
    books.append(book)

# Create libraries
library1 = Library.objects.create(name="Central Public Library")
library2 = Library.objects.create(name="City University Library")
library3 = Library.objects.create(name="Community Library")

# Add books to libraries
library1.books.add(books[0], books[1], books[2], books[4])
library2.books.add(books[2], books[3], books[6])
library3.books.add(books[4], books[5], books[6], books[7])

# Create librarians
Librarian.objects.create(name="Alice Johnson", library=library1)
Librarian.objects.create(name="Bob Smith", library=library2)
Librarian.objects.create(name="Carol Williams", library=library3)

print("Created sample data for testing views:")
print(f"- Authors: {Author.objects.count()}")
print(f"- Books: {Book.objects.count()}")
print(f"- Libraries: {Library.objects.count()}")
print(f"- Librarians: {Librarian.objects.count()}")
print("\nLibrary IDs for testing:")
for lib in Library.objects.all():
    print(f"  - {lib.name}: ID {lib.id}")
print("\nURLs to test:")
print("  - All books: http://localhost:8000/books/")
print("  - Library details: http://localhost:8000/library/1/ (change ID)")
