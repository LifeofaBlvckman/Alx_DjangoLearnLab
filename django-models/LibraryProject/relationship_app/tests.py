"""
Django tests for relationship queries
"""
from django.test import TestCase
from .models import Author, Book, Library, Librarian

class RelationshipTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.author = Author.objects.create(name="George Orwell")
        self.book1 = Book.objects.create(title="1984", author=self.author)
        self.book2 = Book.objects.create(title="Animal Farm", author=self.author)
        
        self.library = Library.objects.create(name="Central Library")
        self.library.books.add(self.book1, self.book2)
        
        self.librarian = Librarian.objects.create(name="John Smith", library=self.library)
    
    def test_foreign_key_query(self):
        """Test querying books by author (ForeignKey)"""
        books = Book.objects.filter(author__name="George Orwell")
        self.assertEqual(books.count(), 2)
        titles = [book.title for book in books]
        self.assertIn("1984", titles)
        self.assertIn("Animal Farm", titles)
    
    def test_many_to_many_query(self):
        """Test listing books in a library (ManyToMany)"""
        books = self.library.books.all()
        self.assertEqual(books.count(), 2)
    
    def test_one_to_one_query(self):
        """Test retrieving librarian for a library (OneToOne)"""
        librarian = Librarian.objects.get(library=self.library)
        self.assertEqual(librarian.name, "John Smith")
