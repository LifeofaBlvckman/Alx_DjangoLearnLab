#!/usr/bin/env python3
"""
Sample queries demonstrating ForeignKey, ManyToMany, and OneToOne relationships
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing relationships"""
    # Create authors
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")
    
    # Create books
    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author2)
    book4 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author2)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Library")
    
    # Add books to libraries
    library1.books.add(book1, book3)
    library2.books.add(book2, book4)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="John Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Jane Doe", library=library2)
    
    return author1, author2, library1, library2

def demonstrate_queries():
    """Demonstrate different types of relationship queries"""
    
    # Create sample data first
    author1, author2, library1, library2 = create_sample_data()
    
    print("=" * 60)
    print("DEMONSTRATING DJANGO ORM RELATIONSHIP QUERIES")
    print("=" * 60)
    
    # 1. ForeignKey relationship: Query all books by a specific author
    print("\n1. FOREIGN KEY RELATIONSHIP")
    print("All books by George Orwell:")
    books_by_orwell = Book.objects.filter(author__name="George Orwell")
    for book in books_by_orwell:
        print(f"  - {book.title}")
    
    # Alternative: Using reverse relationship
    print("\nAlternative (using reverse relationship):")
    for book in author1.books.all():
        print(f"  - {book.title}")
    
    # 2. ManyToMany relationship: List all books in a library
    print("\n\n2. MANYTOMANY RELATIONSHIP")
    print(f"All books in {library1.name}:")
    for book in library1.books.all():
        print(f"  - {book.title} (by {book.author.name})")
    
    # 3. OneToOne relationship: Retrieve the librarian for a library
    print("\n\n3. ONETOONE RELATIONSHIP")
    print(f"Librarian for {library1.name}:")
    try:
        librarian = library1.librarian
        print(f"  - {librarian.name}")
    except Librarian.DoesNotExist:
        print("  - No librarian assigned")
    
    print(f"\nLibrarian for {library2.name}:")
    try:
        librarian = library2.librarian
        print(f"  - {librarian.name}")
    except Librarian.DoesNotExist:
        print("  - No librarian assigned")
    
    # 4. Additional queries for demonstration
    print("\n\n4. ADDITIONAL RELATIONSHIP QUERIES")
    
    # Find which libraries have a specific book
    print(f"\nLibraries that have '1984':")
    book = Book.objects.get(title="1984")
    for library in book.libraries.all():
        print(f"  - {library.name}")
    
    # Find all authors with books in a library
    print(f"\nAuthors with books in {library1.name}:")
    authors_in_library = Author.objects.filter(books__libraries=library1).distinct()
    for author in authors_in_library:
        print(f"  - {author.name}")
    
    print("\n" + "=" * 60)
    print("QUERIES COMPLETED SUCCESSFULLY")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_queries()
