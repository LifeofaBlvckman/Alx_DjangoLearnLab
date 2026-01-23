#!/usr/bin/env python3
"""
Sample queries demonstrating Django ORM relationships as required by the task:
1. Query all books by a specific author (ForeignKey)
2. List all books in a library (ManyToMany)  
3. Retrieve the librarian for a library (OneToOne)
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing"""
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")
    
    # Create books
    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    
    # Add books to libraries
    library1.books.add(book1, book2)
    library2.books.add(book2, book3)
    
    # Create librarians
    Librarian.objects.create(name="Alice Smith", library=library1)
    Librarian.objects.create(name="Bob Johnson", library=library2)
    
    return {
        'authors': [author1, author2],
        'books': [book1, book2, book3],
        'libraries': [library1, library2]
    }

# REQUIRED QUERY 1: Query all books by a specific author (ForeignKey relationship)
def query_books_by_author(author_name):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return []

# REQUIRED QUERY 2: List all books in a library (ManyToMany relationship)
def query_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return []

# REQUIRED QUERY 3: Retrieve the librarian for a library (OneToOne relationship)
def query_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

def main():
    """Run all three required queries and display results"""
    print("=== Creating sample data for demonstration ===")
    data = create_sample_data()
    
    print("\n=== REQUIRED QUERY 1: Query all books by a specific author ===")
    print("Querying all books by 'George Orwell':")
    books = query_books_by_author("George Orwell")
    for book in books:
        print(f"  - {book.title}")
    
    print("\n=== REQUIRED QUERY 2: List all books in a library ===")
    print("Listing all books in 'Central Library':")
    books = query_books_in_library("Central Library")
    for book in books:
        print(f"  - {book.title}")
    
    print("\n=== REQUIRED QUERY 3: Retrieve the librarian for a library ===")
    print("Retrieving librarian for 'Central Library':")
    librarian = query_librarian_for_library("Central Library")
    if librarian:
        print(f"  - Librarian: {librarian.name}")
    else:
        print("  - No librarian found")
    
    print("\n=== All three required queries executed successfully ===")

if __name__ == "__main__":
    main()
