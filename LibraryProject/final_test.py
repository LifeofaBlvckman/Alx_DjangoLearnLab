#!/usr/bin/python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from bookshelf.models import Book

print("=== Final Django CRUD Test ===")
print()

try:
    # Test 1: Create
    print("1. Testing CREATE...")
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        publication_year=2024
    )
    print(f"   Created: {book}")
    
    # Test 2: Retrieve
    print("\n2. Testing RETRIEVE...")
    book_from_db = Book.objects.get(id=book.id)
    print(f"   Retrieved: {book_from_db.title}")
    print(f"   Author: {book_from_db.author}")
    print(f"   Year: {book_from_db.publication_year}")
    
    # Test 3: Update
    print("\n3. Testing UPDATE...")
    book_from_db.title = "Updated Title"
    book_from_db.save()
    print(f"   Updated to: {book_from_db.title}")
    
    # Test 4: Delete
    print("\n4. Testing DELETE...")
    book_from_db.delete()
    count = Book.objects.all().count()
    print(f"   Books remaining: {count}")
    
    print("\n✅ ALL TESTS PASSED!")
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
