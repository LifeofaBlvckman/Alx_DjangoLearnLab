"""
Views for the API application.

This module implements custom views using Django REST Framework's
generic views and mixins for handling CRUD operations efficiently.
Includes permission classes for authentication and authorization.
"""

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    """
    API root endpoint that provides links to available endpoints.
    
    This view is publicly accessible (AllowAny permission) and serves
    as the entry point to the API documentation.
    
    Args:
        request: The HTTP request
        
    Returns:
        Response: JSON with available API endpoints and documentation
    """
    return Response({
        'message': 'Welcome to Advanced API Project with Custom Views',
        'endpoints': {
            'authors': request.build_absolute_uri('authors/'),
            'books': request.build_absolute_uri('books/'),
            'books_create': request.build_absolute_uri('books/create/'),
        },
        'authentication': 'Create, Update, Delete endpoints require authentication',
        'permissions': {
            'public': 'GET /api/books/, GET /api/books/<id>/',
            'authenticated': 'POST /api/books/, PUT/PATCH/DELETE /api/books/<id>/'
        }
    })


# ============================================
# BOOK VIEWS USING GENERIC VIEWS AND MIXINS
# ============================================

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    This view provides read-only access to all books in the system.
    Uses DRF's ListAPIView for efficient list operations with:
    - Pagination (10 items per page)
    - Search functionality
    - Filtering capabilities
    - Public access (AllowAny permission)
    
    Endpoint: GET /api/books/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    
    # Enable filtering and searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    This view provides read-only access to a specific book instance.
    Uses DRF's RetrieveAPIView for efficient single object retrieval.
    
    Endpoint: GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    lookup_field = 'pk'


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    This view handles POST requests to create new book instances.
    Includes custom validation from BookSerializer.
    Restricted to authenticated users only.
    
    Customization:
    - Overrides perform_create to add custom logic
    - Returns 201 Created on success with book data
    - Uses IsAuthenticated permission
    
    Endpoint: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required
    
    def perform_create(self, serializer):
        """
        Customize the creation process.
        
        This method is called when a book is being created.
        Can be extended to add custom logic like:
        - Setting created_by user
        - Logging creation activity
        - Sending notifications
        
        Args:
            serializer: The BookSerializer instance
        """
        # You could add custom logic here, e.g.:
        # book = serializer.save(created_by=self.request.user)
        serializer.save()
        
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response.
        
        This extends the default create behavior to provide
        custom response formatting if needed.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    This view handles PUT and PATCH requests to update book instances.
    PUT requires all fields, PATCH allows partial updates.
    Restricted to authenticated users only.
    
    Customization:
    - Handles both full (PUT) and partial (PATCH) updates
    - Returns custom response format
    - Uses IsAuthenticated permission
    
    Endpoint: PUT/PATCH /api/books/<int:pk>/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response.
        
        This extends the default update behavior to provide
        custom response formatting and additional validation.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Book updated successfully',
                'book': serializer.data
            },
            status=status.HTTP_200_OK
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    This view handles DELETE requests to remove book instances.
    Restricted to authenticated users only.
    
    Customization:
    - Overrides destroy method for custom response
    - Returns 204 No Content on success
    - Uses IsAuthenticated permission
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required
    lookup_field = 'pk'
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize response.
        
        This extends the default delete behavior to provide
        custom response formatting and additional cleanup.
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================
# COMBINED BOOK VIEW (All CRUD operations in one)
# ============================================

class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined List and Create view for Books.
    
    This view demonstrates handling both list and create operations
    in a single class with different permissions per method.
    
    Endpoints:
    - GET /api/books-combined/ (public)
    - POST /api/books-combined/ (authenticated)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Apply different permissions based on HTTP method.
        
        - GET: AllowAny (public read access)
        - POST: IsAuthenticated (authentication required for creation)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined Retrieve, Update, and Destroy view for Books.
    
    This view demonstrates handling RUD operations in a single class
    with different permissions per method.
    
    Endpoints:
    - GET /api/books-combined/<id>/ (public)
    - PUT/PATCH/DELETE /api/books-combined/<id>/ (authenticated)
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'
    
    def get_permissions(self):
        """
        Apply different permissions based on HTTP method.
        
        - GET: AllowAny (public read access)
        - PUT, PATCH, DELETE: IsAuthenticated (auth required for modifications)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


# ============================================
# AUTHOR VIEWS
# ============================================

class AuthorListCreate(generics.ListCreateAPIView):
    """
    Combined List and Create view for Authors.
    
    Demonstrates a different approach by combining list and create
    in a single view with different permissions per method.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Apply different permissions based on HTTP method.
        
        - GET: AllowAny (public read)
        - POST: IsAuthenticated (auth required for creation)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined Retrieve, Update, and Destroy view for Authors.
    
    Demonstrates a different approach by combining RUD operations
    in a single view with different permissions per method.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Apply different permissions based on HTTP method.
        
        - GET: AllowAny (public read)
        - PUT/PATCH/DELETE: IsAuthenticated (auth required for modifications)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
