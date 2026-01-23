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
