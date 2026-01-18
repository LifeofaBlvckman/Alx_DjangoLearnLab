from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    from .models import Book
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimize query by prefetching related books and their authors
        return Library.objects.prefetch_related('books__author')
