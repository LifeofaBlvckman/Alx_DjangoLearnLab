from django.contrib import admin
from .models import Author, Book, Library, Librarian

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')
    filter_horizontal = ('books',)
    search_fields = ('name',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')
