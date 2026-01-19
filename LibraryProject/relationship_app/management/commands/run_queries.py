from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Demonstrate Django ORM relationship queries as per task requirements'
    
    def handle(self, *args, **kwargs):
        # Clear any existing data
        Author.objects.all().delete()
        Book.objects.all().delete()
        Library.objects.all().delete()
        Librarian.objects.all().delete()
        
        self.stdout.write("=" * 60)
        self.stdout.write("CREATING SAMPLE DATA FOR RELATIONSHIP DEMONSTRATION")
        self.stdout.write("=" * 60)
        
        # Create sample data
        author1 = Author.objects.create(name="George Orwell")
        author2 = Author.objects.create(name="J.K. Rowling")
        
        book1 = Book.objects.create(title="1984", author=author1)
        book2 = Book.objects.create(title="Animal Farm", author=author1)
        book3 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author2)
        book4 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author2)
        
        library1 = Library.objects.create(name="Central Library")
        library2 = Library.objects.create(name="City Library")
        
        library1.books.add(book1, book3)
        library2.books.add(book2, book4)
        
        Librarian.objects.create(name="John Smith", library=library1)
        Librarian.objects.create(name="Jane Doe", library=library2)
        
        self.stdout.write("\n✓ Sample data created successfully!")
        self.stdout.write("  - Authors: George Orwell, J.K. Rowling")
        self.stdout.write("  - Books: 4 books created")
        self.stdout.write("  - Libraries: Central Library, City Library")
        self.stdout.write("  - Librarians: John Smith, Jane Doe")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("DEMONSTRATING REQUIRED QUERIES")
        self.stdout.write("=" * 60)
        
        # 1. Query all books by a specific author (ForeignKey relationship)
        self.stdout.write("\n1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR (ForeignKey):")
        self.stdout.write("   All books by George Orwell:")
        books_by_orwell = Book.objects.filter(author__name="George Orwell")
        for i, book in enumerate(books_by_orwell, 1):
            self.stdout.write(f"   {i}. {book.title}")
        
        # 2. List all books in a library (ManyToMany relationship)
        self.stdout.write("\n2. LIST ALL BOOKS IN A LIBRARY (ManyToMany):")
        self.stdout.write(f"   All books in {library1.name}:")
        for i, book in enumerate(library1.books.all(), 1):
            self.stdout.write(f"   {i}. {book.title}")
        
        # 3. Retrieve the librarian for a library (OneToOne relationship)
        self.stdout.write("\n3. RETRIEVE THE LIBRARIAN FOR A LIBRARY (OneToOne):")
        self.stdout.write(f"   Librarian for {library1.name}:")
        librarian = Librarian.objects.get(library=library1)
        self.stdout.write(f"   - {librarian.name}")
        
        self.stdout.write(f"\n   Librarian for {library2.name}:")
        librarian = Librarian.objects.get(library=library2)
        self.stdout.write(f"   - {librarian.name}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("ADDITIONAL DEMONSTRATION QUERIES")
        self.stdout.write("=" * 60)
        
        # Additional useful queries
        self.stdout.write("\nA. Find author of a specific book:")
        book = Book.objects.get(title="1984")
        self.stdout.write(f"   Author of '1984': {book.author.name}")
        
        self.stdout.write("\nB. Find libraries containing a specific book:")
        book = Book.objects.get(title="Animal Farm")
        libraries_with_book = Library.objects.filter(books=book)
        self.stdout.write(f"   Libraries with 'Animal Farm':")
        for lib in libraries_with_book:
            self.stdout.write(f"   - {lib.name}")
        
        self.stdout.write("\nC. Find all books by an author (using reverse relationship):")
        self.stdout.write(f"   All books by {author2.name} (using author.books.all()):")
        for book in author2.books.all():
            self.stdout.write(f"   - {book.title}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("QUERIES COMPLETED SUCCESSFULLY!")
        self.stdout.write("=" * 60)
