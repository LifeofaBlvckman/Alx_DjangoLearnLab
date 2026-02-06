# ALX Task: Custom Views with Django REST Framework

## ✅ Task Requirements Completed

### 1. Generic Views Implemented:
- BookListView (ListAPIView)
- BookDetailView (RetrieveAPIView)
- BookCreateView (CreateAPIView)
- BookUpdateView (UpdateAPIView)
- BookDeleteView (DestroyAPIView)

### 2. URL Patterns Configured in api/urls.py
- GET /api/books/ - List books
- GET /api/books/<id>/ - Book detail
- POST /api/books/create/ - Create book (auth required)
- PUT/PATCH /api/books/<id>/update/ - Update book (auth required)
- DELETE /api/books/<id>/delete/ - Delete book (auth required)

### 3. Permissions Implemented
- Public read access (AllowAny)
- Authenticated write access (IsAuthenticated)

### 4. Validation Working
- Custom validate_publication_year() prevents future years

## 🚀 Testing
```bash
python manage.py runserver 8002
curl http://127.0.0.1:8002/api/books/
curl -X POST http://127.0.0.1:8002/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","publication_year":2020,"author":1}'
```

**Project complete-f README_GENERIC_VIEWS.md test_views.py*
