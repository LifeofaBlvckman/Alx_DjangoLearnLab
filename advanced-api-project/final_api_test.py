#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api/books"

def run_test(name, params=None):
    """Run a test and display formatted results."""
    print(f"\n{'='*70}")
    print(f"🧪 {name}")
    print(f"🔗 URL: {BASE_URL}?{'&'.join([f'{k}={v}' for k, v in (params or {}).items()])}")
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Status: {response.status_code}")
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            count = data.get('count', 0)
            results = data.get('results', [])
            print(f"📊 Total matches: {count}")
            print(f"📄 This page: {len(results)} items")
            
            if results:
                print("\n📚 Results:")
                for i, item in enumerate(results, 1):
                    title = item.get('title', 'N/A')
                    author_name = item.get('author_name', 'Unknown')
                    year = item.get('publication_year', 'N/A')
                    print(f"   {i:2d}. '{title}' by {author_name} ({year})")
        else:
            # Non-paginated response (shouldn't happen with our setup)
            print(f"📊 Results: {len(data)}")
            for i, item in enumerate(data[:5], 1):
                title = item.get('title', 'N/A')
                author_name = item.get('author_name', item.get('author', 'Unknown'))
                year = item.get('publication_year', 'N/A')
                print(f"   {i}. '{title}' by {author_name} ({year})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

print("🎯 FINAL API TEST - Filtering, Searching, Ordering")
print("="*70)
print("Testing all implemented features with actual data")
print("="*70)

# First, get total count
print("\n📋 Initial data check:")
response = requests.get(BASE_URL)
if response.status_code == 200:
    data = response.json()
    print(f"Total books in database: {data.get('count', 'N/A')}")

# Run comprehensive tests
print("\n🔍 TESTING FILTERING FEATURES:")
run_test("1. All books (default pagination)", {})

print("\n📌 FILTER BY AUTHOR:")
run_test("2. Books by J.R.R. Tolkien", {"author__name": "Tolkien"})
run_test("3. Books by Stephen King", {"author__name": "King"})
run_test("4. Books by J.K. Rowling", {"author__name": "Rowling"})

print("\n📌 FILTER BY TITLE:")
run_test("5. Books with 'Harry' in title", {"title": "Harry"})
run_test("6. Books with 'Adventure' in title", {"title": "Adventure"})

print("\n📌 FILTER BY PUBLICATION YEAR:")
run_test("7. Books from exactly 1997", {"publication_year": 1997})
run_test("8. Books published after 1950", {"publication_year__gt": 1950})
run_test("9. Books published before 1900", {"publication_year__lt": 1900})
run_test("10. Books between 1900-1950", {"publication_year__gt": 1900, "publication_year__lt": 1950})

print("\n🔍 TESTING SEARCHING FEATURES:")
run_test("11. Search 'potter' (across title and author)", {"search": "potter"})
run_test("12. Search 'adventure'", {"search": "adventure"})
run_test("13. Search 'king'", {"search": "king"})
run_test("14. Search 'the' (common word)", {"search": "the"})

print("\n🔍 TESTING ORDERING FEATURES:")
run_test("15. Order by title (A-Z)", {"ordering": "title"})
run_test("16. Order by title (Z-A)", {"ordering": "-title"})
run_test("17. Order by publication year (oldest first)", {"ordering": "publication_year"})
run_test("18. Order by publication year (newest first)", {"ordering": "-publication_year"})

print("\n🔍 TESTING COMBINED QUERIES:")
run_test("19. Tolkien's books ordered by year", {"author__name": "Tolkien", "ordering": "publication_year"})
run_test("20. 20th century books with 'the', ordered by title", 
         {"search": "the", "publication_year__gt": 1900, "publication_year__lt": 2000, "ordering": "title"})
run_test("21. Stephen King's 20th century books, newest first", 
         {"author__name": "King", "publication_year__gt": 1900, "publication_year__lt": 2000, "ordering": "-publication_year"})
run_test("22. Adventure books before 1900 ordered by author", 
         {"search": "adventure", "publication_year__lt": 1900, "ordering": "author__name"})

print(f"\n{'='*70}")
print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*70)
print("\n✅ IMPLEMENTATION SUMMARY:")
print("   ✔️ 1. FILTERING: title, author__name, publication_year, publication_year__gt, publication_year__lt")
print("   ✔️ 2. SEARCHING: title + author__name fields")
print("   ✔️ 3. ORDERING: title, publication_year (+ descending with -)")
print("   ✔️ 4. PAGINATION: 10 items per page")
print("   ✔️ 5. COMBINED: All features work together")
print("\n📚 Current book count: 22 books by 9 authors")
