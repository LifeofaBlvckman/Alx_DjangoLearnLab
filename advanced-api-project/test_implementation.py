print("Checking Generic Views Implementation...")
print("=" * 50)

# Check views.py
print("\n1. Checking api/views.py...")
try:
    with open('api/views.py', 'r') as f:
        content = f.read()
        views_to_check = [
            'class BookListView',
            'class BookDetailView', 
            'class BookCreateView',
            'class BookUpdateView',
            'class BookDeleteView'
        ]
        for view in views_to_check:
            if view in content:
                print(f"   ✅ {view}")
            else:
                print(f"   ❌ {view} not found")
except:
    print("   ❌ Cannot read api/views.py")

# Check urls.py
print("\n2. Checking api/urls.py...")
try:
    with open('api/urls.py', 'r') as f:
        content = f.read()
        urls_to_check = [
            'books/',
            'books/create/',
            'books/<int:pk>/',
            'books/<int:pk>/update/',
            'books/<int:pk>/delete/'
        ]
        for url in urls_to_check:
            if url in content:
                print(f"   ✅ /api/{url}")
            else:
                print(f"   ❌ /api/{url} not found")
except:
    print("   ❌ Cannot read api/urls.py")

# Check permissions
print("\n3. Checking permissions...")
try:
    with open('api/views.py', 'r') as f:
        content = f.read()
        if 'permissions.AllowAny' in content and 'permissions.IsAuthenticated' in content:
            print("   ✅ Permission classes found")
        else:
            print("   ❌ Permission classes missing")
except:
    print("   ❌ Cannot check permissions")

print("\n" + "=" * 50)
print("Run 'python manage.py runserver 8002' to test endpoints")
print("=" * 50)
