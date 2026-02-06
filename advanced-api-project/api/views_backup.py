"""
Views for the API application.

This module provides API endpoints for the Author and Book models
using Django REST Framework's generic views for common operations.
"""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint that provides links to available endpoints.
    
    Args:
        request: The HTTP request
        
    Returns:
        Response: JSON with available API endpoints
    """
    return Response({
        'authors': request.build_absolute_uri('authors/'),
        'books': request.build_absolute_uri('books/'),
        'message': 'Welcome to the Advanced API Project'
    })


class AuthorListCreate(generics.ListCreateAPIView):
    """
    List all authors or create a new author.
    
    This view handles:
        - GET /api/authors/: Returns a list of all authors with their books
        - POST /api/authors/: Creates a new author
    
    Uses AuthorSerializer which includes nested book serialization.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an author instance.
    
    This view handles:
        - GET /api/authors/<id>/: Get a specific author
        - PUT /api/authors/<id>/: Update an author
        - PATCH /api/authors/<id>/: Partially update an author
        - DELETE /api/authors/<id>/: Delete an author
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer


class BookListCreate(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    
    This view handles:
        - GET /api/books/: Returns a list of all books
        - POST /api/books/: Creates a new book (with validation)
    
    Uses BookSerializer which includes custom validation for publication_year.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a book instance.
    
    This view handles:
        - GET /api/books/<id>/: Get a specific book
        - PUT /api/books/<id>/: Update a book
        - PATCH /api/books/<id>/: Partially update a book
        - DELETE /api/books/<id>/: Delete a book
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
