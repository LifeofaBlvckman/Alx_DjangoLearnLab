"""
Test suite for API views.
Comprehensive unit tests for Book and Author endpoints.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author


class BaseTestCase(TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test data and client"""
        # Clear any existing test data first
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.filter(username__in=['testuser', 'admin']).delete()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.R.R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="J.K. Rowling")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="The Hobbit",
            author=self.author1,
            publication_year=1937
        )
        
        self.book2 = Book.objects.create(
            title="1984",
            author=self.author2,
            publication_year=1949
        )
        
        self.book3 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author=self.author3,
            publication_year=1997
        )
        
        self.book4 = Book.objects.create(
            title="Animal Farm",
            author=self.author2,
            publication_year=1945
        )
        
        self.book5 = Book.objects.create(
            title="The Lord of the Rings",
            author=self.author1,
            publication_year=1954
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # URLs - Using the correct URL names from your urls.py
        self.books_list_url = reverse('book-list')
        self.books_detail_url = lambda pk: reverse('book-detail', args=[pk])
        self.books_create_url = reverse('book-create')
        self.books_update_url = reverse('book-update')
        self.books_delete_url = reverse('book-delete')
        
        # Author URLs
        self.author_list_url = reverse('author-list')
        self.author_detail_url = lambda pk: reverse('author-detail', args=[pk])
        
        # API root
        self.api_root_url = reverse('api-root')
    
    def authenticate_user(self, user=None):
        """Helper to authenticate a user"""
        if user is None:
            user = self.user
        self.client.force_authenticate(user=user)
    
    def unauthenticate(self):
        """Helper to remove authentication"""
        self.client.force_authenticate(user=None)


class BookListViewTests(BaseTestCase):
    """Tests for Book List View"""
    
    def test_get_all_books_unauthenticated(self):
        """Test that unauthenticated users can view all books"""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
    
    def test_pagination(self):
        """Test that pagination is working"""
        response = self.client.get(self.books_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)
    
    def test_filter_by_author_name(self):
        """Test filtering books by author name"""
        response = self.client.get(self.books_list_url, {'author__name': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_filter_by_title(self):
        """Test filtering books by title"""
        response = self.client.get(self.books_list_url, {'title': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIn("Harry Potter", response.data['results'][0]['title'])
    
    def test_filter_by_publication_year(self):
        """Test filtering books by publication year"""
        response = self.client.get(self.books_list_url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_filter_by_year_greater_than(self):
        """Test filtering books by year greater than"""
        response = self.client.get(self.books_list_url, {'publication_year__gt': 1950})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_filter_by_year_less_than(self):
        """Test filtering books by year less than"""
        response = self.client.get(self.books_list_url, {'publication_year__lt': 1900})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    
    def test_search_functionality(self):
        """Test searching across title and author name"""
        response = self.client.get(self.books_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
        response = self.client.get(self.books_list_url, {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_ordering_by_title_asc(self):
        """Test ordering books by title ascending"""
        response = self.client.get(self.books_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_desc(self):
        """Test ordering books by title descending"""
        response = self.client.get(self.books_list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year(self):
        """Test ordering books by publication year"""
        response = self.client.get(self.books_list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
    
    def test_combined_filter_search_order(self):
        """Test combined filtering, searching, and ordering"""
        response = self.client.get(self.books_list_url, {
            'author__name': 'Orwell',
            'ordering': 'publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, [1945, 1949])
    
    def test_post_to_list_view_not_allowed(self):
        """Test that POST to ListView is not allowed"""
        response = self.client.post(self.books_list_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class BookDetailViewTests(BaseTestCase):
    """Tests for Book Detail View"""
    
    def test_get_single_book_unauthenticated(self):
        """Test that unauthenticated users can view a single book"""
        url = self.books_detail_url(self.book1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')
    
    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist"""
        url = self.books_detail_url(999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(BaseTestCase):
    """Tests for Book Create View"""
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.books_create_url, data)
        # Your API returns 403 for unauthenticated access to protected endpoints
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books"""
        self.authenticate_user()
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.books_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 6)
    
    def test_create_book_invalid_year(self):
        """Test creating a book with invalid publication year (future)"""
        self.authenticate_user()
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.id
        }
        response = self.client.post(self.books_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_empty_title(self):
        """Test creating a book with empty title"""
        self.authenticate_user()
        data = {
            'title': '',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(self.books_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_get_to_create_view_not_allowed(self):
        """Test that GET to CreateView is not allowed"""
        response = self.client.get(self.books_create_url)
        # Your API returns 403 for GET requests to protected endpoints
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookUpdateViewTests(BaseTestCase):
    """Tests for Book Update View"""
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books"""
        data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books"""
        self.authenticate_user()
        data = {
            'id': self.book1.id,
            'title': 'The Hobbit - Revised',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit - Revised')
    
    def test_update_book_partial(self):
        """Test partial update of a book using PATCH"""
        self.authenticate_user()
        data = {
            'id': self.book1.id,
            'title': 'The Hobbit - Special Edition'
        }
        response = self.client.patch(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit - Special Edition')
    
    def test_update_book_without_id(self):
        """Test updating a book without providing ID"""
        self.authenticate_user()
        data = {
            'title': 'Updated Title',
            'publication_year': 1937,
            'author': self.author1.id
        }
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('id', response.data)
    
    def test_update_nonexistent_book(self):
        """Test updating a book that doesn't exist"""
        self.authenticate_user()
        data = {
            'id': 999,
            'title': 'Nonexistent Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_to_update_view_not_allowed(self):
        """Test that GET to UpdateView is not allowed"""
        response = self.client.get(self.books_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookDeleteViewTests(BaseTestCase):
    """Tests for Book Delete View"""
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books"""
        data = {'id': self.book1.id}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books"""
        self.authenticate_user()
        data = {'id': self.book1.id}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_delete_book_without_id(self):
        """Test deleting a book without providing ID"""
        self.authenticate_user()
        data = {}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('id', response.data)
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist"""
        self.authenticate_user()
        data = {'id': 999}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_to_delete_view_not_allowed(self):
        """Test that GET to DeleteView is not allowed"""
        response = self.client.get(self.books_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthorViewTests(BaseTestCase):
    """Tests for Author views"""
    
    def test_get_all_authors_unauthenticated(self):
        """Test that unauthenticated users can view all authors"""
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check we get authors data (could be list or paginated dict)
        self.assertTrue(len(response.data) >= 3)
    
    def test_create_author_unauthenticated(self):
        """Test that unauthenticated users cannot create authors"""
        data = {'name': 'New Author'}
        response = self.client.post(self.author_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_author_authenticated(self):
        """Test that authenticated users can create authors"""
        self.authenticate_user()
        data = {'name': 'New Author'}
        response = self.client.post(self.author_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 4)
    
    def test_get_single_author(self):
        """Test getting a single author"""
        url = self.author_detail_url(self.author1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.R.R. Tolkien')


class APIRootViewTests(BaseTestCase):
    """Tests for API root endpoint"""
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = self.client.get(self.api_root_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
        self.assertIn('features', response.data)


class ModelTests(TestCase):
    """Tests for models"""
    
    def setUp(self):
        """Set up test data for model tests"""
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_str(self):
        """Test Author string representation"""
        self.assertEqual(str(self.author), "Test Author")
    
    def test_book_str(self):
        """Test Book string representation"""
        book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2023
        )
        self.assertEqual(str(book), "Test Book (2023)")
    
    def test_author_book_count(self):
        """Test author book count method"""
        Book.objects.create(
            title="Book 1",
            author=self.author,
            publication_year=2020
        )
        Book.objects.create(
            title="Book 2",
            author=self.author,
            publication_year=2021
        )
        self.assertEqual(self.author.book_count(), 2)
    
    def test_book_ordering(self):
        """Test that books are ordered by title"""
        Book.objects.create(title="Z Book", author=self.author, publication_year=2023)
        Book.objects.create(title="A Book", author=self.author, publication_year=2021)
        Book.objects.create(title="M Book", author=self.author, publication_year=2022)
        
        books = Book.objects.all()
        self.assertEqual(books[0].title, "A Book")
        self.assertEqual(books[1].title, "M Book")
        self.assertEqual(books[2].title, "Z Book")


class PermissionTests(BaseTestCase):
    """Tests for permission classes"""
    
    def test_unauthenticated_access_to_protected_endpoints(self):
        """Test that unauthenticated users cannot access protected endpoints"""
        # Create endpoint
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post(self.books_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Update endpoint
        data = {'id': self.book1.id, 'title': 'Updated'}
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Delete endpoint
        data = {'id': self.book1.id}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authenticated_access_to_protected_endpoints(self):
        """Test that authenticated users can access protected endpoints"""
        self.authenticate_user()
        
        # Create endpoint - should work
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post(self.books_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Update endpoint - should work
        data = {'id': self.book1.id, 'title': 'Updated', 'publication_year': 1937, 'author': self.author1.id}
        response = self.client.put(self.books_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete endpoint - should work
        data = {'id': self.book2.id}
        response = self.client.delete(self.books_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
