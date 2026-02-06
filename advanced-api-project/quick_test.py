import requests
import json

BASE = "http://localhost:8000/api/books"

def test(name, params):
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"Params: {params}")
    
    r = requests.get(BASE, params=params)
    if r.status_code == 200:
        data = r.json()
        count = data.get('count', len(data.get('results', [])))
        print(f"✅ Success: {count} results")
        
        if count > 0:
            # Show first result details
            first = data.get('results', [data])[0]
            print(f"   First: '{first.get('title')}' by {first.get('author', {}).get('name', 'N/A')}")
    else:
        print(f"❌ Failed: {r.status_code}")
        print(r.text[:200])
    return r

print("📚 Testing API Filtering, Searching, Ordering")
print("="*60)

# Basic tests
test("All books", {})
test("Filter by author (Tolkien)", {"author__name": "Tolkien"})
test("Filter by title (Harry)", {"title": "Harry"})
test("Filter by year (1997)", {"publication_year": 1997})
test("Filter year > 1950", {"publication_year__gt": 1950})
test("Filter year < 1900", {"publication_year__lt": 1900})
test("Search 'potter'", {"search": "potter"})
test("Search 'adventure'", {"search": "adventure"})
test("Order by title", {"ordering": "title"})
test("Order by -year", {"ordering": "-publication_year"})
test("Order by author", {"ordering": "author__name"})

# Combined tests
test("Tolkien + order by year", {"author__name": "Tolkien", "ordering": "publication_year"})
test("Search 'the' + year > 1900", {"search": "the", "publication_year__gt": 1900})
test("Complex: King's 20th century books", {"author__name": "King", "publication_year__gt": 1900, "publication_year__lt": 2000})

print(f"\n{'='*60}")
print("🎉 All tests completed!")
