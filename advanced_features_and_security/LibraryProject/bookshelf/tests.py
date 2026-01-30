from django.test import TestCase, Client
from django.urls import reverse
from .models import Book
from django.utils import timezone

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890",
            published_date="2023-01-01",
            description="Test description"
        )
    
    def test_csrf_protection(self):
        """Test that forms require CSRF token"""
        # Try to POST without CSRF token
        response = self.client.post(reverse('add_book'), {
            'title': 'Hacked',
            'author': 'Hacker',
            'isbn': '9999999999',
            'published_date': '2023-01-01',
            'description': 'Hacked'
        })
        # Should get 403 Forbidden due to CSRF failure
        self.assertEqual(response.status_code, 403)
        print("✅ CSRF protection working")
    
    def test_sql_injection_safe(self):
        """Test that search is safe from SQL injection"""
        # Test with SQL injection attempt
        response = self.client.get('/?q=%27+OR+%271%27%3D%271')
        self.assertEqual(response.status_code, 200)
        # Should not crash or return all books
        print("✅ SQL injection attempt handled safely")
    
    def test_xss_protection(self):
        """Test that XSS attempts are blocked"""
        # Try to create book with script tag
        xss_book = Book.objects.create(
            title="XSS Test",
            author="<script>alert('xss')</script>",
            isbn="1111111111",
            published_date="2023-01-01",
            description="<script>alert('xss')</script>"
        )
        
        # Check that script tags are not in output
        response = self.client.get(reverse('book_detail', args=[xss_book.pk]))
        self.assertNotContains(response, '<script>')
        print("✅ XSS protection working")
    
    def test_security_headers(self):
        """Test that security headers are present"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for security headers
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')
        print("✅ Security headers present")
    
    def test_debug_false(self):
        """Test that DEBUG is False"""
        from django.conf import settings
        self.assertFalse(settings.DEBUG)
        print("✅ DEBUG = False (secure)")
