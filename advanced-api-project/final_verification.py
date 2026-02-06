print("=" * 60)
print("FINAL ALX TASK VERIFICATION")
print("=" * 60)

print("\n✅ 1. Checking URLs in api/urls.py:")
import re

with open('api/urls.py', 'r') as f:
    content = f.read()
    
# Look for book-related URLs
book_urls = re.findall(r"path\('books/[^']*'", content)

print("Found book URLs:")
for url in book_urls:
    print(f"   {url})")

print("\n✅ 2. Checking for correct URL patterns:")
required_patterns = [
    "path('books/update/",
    "path('books/delete/"
]

all_correct = True
for pattern in required_patterns:
    if pattern in content:
        print(f"   ✅ {pattern}...')")
    else:
        print(f"   ❌ {pattern}...') - NOT FOUND")
        all_correct = False

print("\n✅ 3. Checking view classes in api/views.py:")
required_views = ["ListView", "DetailView", "CreateView", "UpdateView", "DeleteView"]

with open('api/views.py', 'r') as f:
    views_content = f.read()

for view in required_views:
    if f"class {view}(" in views_content:
        print(f"   ✅ {view}")
    else:
        print(f"   ❌ {view} - NOT FOUND")
        all_correct = False

print("\n" + "=" * 60)
if all_correct:
    print("🎉 ALL REQUIREMENTS MET!")
    print("✅ URLs: /books/update/ and /books/delete/ (correct)")
    print("✅ Views: All 5 required view classes present")
    print("✅ Project is ready for ALX submission!")
else:
    print("⚠️  Some requirements missing")
print("=" * 60)
