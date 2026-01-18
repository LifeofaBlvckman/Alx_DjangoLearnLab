#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear and create fresh data
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create data
author = Author.objects.create(name="George Orwell")
book1 = Book.objects.create(title="1984", author=author)
book2 = Book.objects.create(title="Animal Farm", author=author)

library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

Librarian.objects.create(name="John Smith", library=library)

# Execute and print results
# 1. ForeignKey query
books = Book.objects.filter(author__name="George Orwell")
for book in books:
    print(book.title)

# 2. ManyToMany query  
print("---")  # Separator
for book in library.books.all():
    print(book.title)

# 3. OneToOne query
print("---")  # Separator
librarian = Librarian.objects.get(library=library)
print(librarian.name)
