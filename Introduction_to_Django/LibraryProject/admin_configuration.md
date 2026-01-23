# Django Admin Configuration for Book Model

## 1. Registered Book Model in admin.py
\`\`\`python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable search by title and author
    search_fields = ('title', 'author')
    
    # Add filters for publication year
    list_filter = ('publication_year',)
    
    # Fields to display in the detail/edit view
    fields = ('title', 'author', 'publication_year')
    
    # Optional: ordering
    ordering = ('title',)
\`\`\`

## 2. Superuser Information
- Username: `ola` (already exists)
- Use existing password

## 3. Admin Interface Features Configured:
- **List Display**: Shows title, author, and publication year
- **Search**: Search books by title or author  
- **Filters**: Filter books by publication year
- **Fields**: Custom fields in detail/edit view
- **Ordering**: Books ordered alphabetically by title

## 4. Accessing the Admin:
1. Run server: \`python manage.py runserver\`
2. Navigate to: \`http://localhost:8000/admin/\`
3. Login with username: \`ola\`
4. Click "Books" to manage book entries

## 5. Expected Admin Capabilities:
- View all books with title, author, year columns
- Search for specific books
- Filter by publication year
- Add new books
- Edit existing books
- Delete books
