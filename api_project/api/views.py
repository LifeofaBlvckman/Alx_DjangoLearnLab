from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

# Existing view for backward compatibility
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Add permission

# New ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations
    
    # Optional: Different permissions for different actions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]  # Only admins can create/update/delete
        return [permission() for permission in permission_classes]
