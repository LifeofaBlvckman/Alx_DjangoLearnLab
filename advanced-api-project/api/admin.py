"""
Admin configuration for the API application.

This module registers the Author and Book models with the Django admin
interface, providing a user-friendly way to manage data.
"""

from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Author model.
    
    Features:
        - List display with ID and name
        - Search functionality by name
        - Filtering options
        - Display of book count in list view
    """
    list_display = ['id', 'name', 'book_count']
    search_fields = ['name']
    list_filter = ['name']
    
    def book_count(self, obj):
        """
        Custom admin column showing number of books by author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            int: Number of books by this author
        """
        return obj.book_count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Book model.
    
    Features:
        - List display with ID, title, year, and author
        - Search functionality by title and author name
        - Filtering by publication year and author
        - Fieldsets for organized form display
    """
    list_display = ['id', 'title', 'publication_year', 'author']
    search_fields = ['title', 'author__name']
    list_filter = ['publication_year', 'author']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'publication_year', 'author')
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize queryset by selecting related authors.
        
        Args:
            request: The current request
            
        Returns:
            QuerySet: Optimized queryset
        """
        return super().get_queryset(request).select_related('author')
