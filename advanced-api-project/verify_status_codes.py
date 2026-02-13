#!/usr/bin/env python3
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')

import django
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Author

print("Verifying Status Codes...")
print("=" * 60)

class StatusCodeVerification(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2023
        )
        self.client = APIClient()
    
    def test_status_codes(self):
        tests = [
            ("GET book list", reverse('book-list'), None, status.HTTP_200_OK),
            ("GET book detail", reverse('book-detail', args=[self.book.id]), None, status.HTTP_200_OK),
            ("POST create book (unauthenticated)", reverse('book-create'), 
             {'title': 'New', 'publication_year': 2023, 'author': self.author.id}, status.HTTP_403_FORBIDDEN),
            ("GET non-existent book", reverse('book-detail', args=[999]), None, status.HTTP_404_NOT_FOUND),
        ]
        
        for name, url, data, expected in tests:
            if data:
                if 'POST' in name:
                    response = self.client.post(url, data)
                elif 'PUT' in name:
                    response = self.client.put(url, data)
                elif 'DELETE' in name:
                    response = self.client.delete(url, data)
                else:
                    response = self.client.get(url, data)
            else:
                response = self.client.get(url)
            
            if response.status_code == expected:
                print(f"✅ {name}: {response.status_code} == {expected}")
            else:
                print(f"❌ {name}: {response.status_code} != {expected}")

if __name__ == "__main__":
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(StatusCodeVerification)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n" + "=" * 60)
        print("✅ All status codes are correct!")
    else:
        print("\n" + "=" * 60)
        print("❌ Some status codes are incorrect")
