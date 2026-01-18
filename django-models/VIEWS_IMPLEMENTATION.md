# Django Views Implementation - Task Completion

## Overview
Successfully implemented both function-based and class-based views in Django as per the task requirements.

## Files Modified/Created

### 1. Views (relationship_app/views.py)
- **Function-based view**: `list_books()` - displays all books with authors
- **Class-based view**: `LibraryDetailView` - displays specific library details

### 2. URL Configuration
- **relationship_app/urls.py**: New file with URL patterns
  - `path('books/', views.list_books, name='list_books')`
  - `path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail')`
- **LibraryProject/urls.py**: Updated to include relationship_app URLs

### 3. Templates
- **list_books.html**: Template for function-based view
- **library_detail.html**: Template for class-based view

### 4. Models
- **Book model**: Added `publication_year` field
- **Migration**: Created 0002_book_publication_year.py

### 5. Test Data
- **create_test_data.py**: Script to populate database with sample data

## Testing
- Function-based view: `http://127.0.0.1:8000/books/` (HTTP 200)
- Class-based view: `http://127.0.0.1:8000/library/7/` (HTTP 200)

## Key Learnings
1. Creating both function-based and class-based views
2. Configuring URL patterns in Django
3. Using Django's generic class-based views (DetailView)
4. Template rendering with context
5. Database query optimization
6. Model migrations
