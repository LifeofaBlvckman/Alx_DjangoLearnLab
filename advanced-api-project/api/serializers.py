"""
Serializers for the API application.

This module defines serializers that handle complex data structures,
nested relationships, and custom validation for the Book and Author models.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer
    
    Serializes Book model instances to JSON format and handles deserialization
    from JSON back to model instances. Includes custom validation logic
    for the publication_year field.
    
    Fields:
        - id: Auto-generated primary key
        - title: Book title
        - publication_year: Year of publication
        - author: Foreign key to Author model
        - author_name: Read-only field showing author's name
    
    Validation:
        Custom validation ensures publication_year is not in the future.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']
        read_only_fields = ['id', 'author_name']
    
    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        
        This custom validation method ensures data integrity by preventing
        books from having publication dates in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year if valid
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
            
        Example:
            >>> If current year is 2024 and value is 2025
            >>> Raises: ValidationError("Publication year cannot be in the future...")
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
    
    def validate(self, data):
        """
        Object-level validation for Book data.
        
        This method validates the entire object, allowing checks that involve
        multiple fields. Currently validates that title is not empty.
        
        Args:
            data (dict): The data to validate
            
        Returns:
            dict: The validated data
        """
        # Ensure title is not just whitespace
        if 'title' in data and not data['title'].strip():
            raise serializers.ValidationError({
                'title': 'Title cannot be empty or just whitespace.'
            })
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer
    
    Serializes Author model instances with nested BookSerializer to show
    related books. Demonstrates handling of nested relationships in DRF.
    
    Fields:
        - id: Auto-generated primary key
        - name: Author's name
        - books: Nested serialization of related books (read-only)
        - book_count: Read-only field showing number of books
    
    Relationship Handling:
        The 'books' field uses BookSerializer with many=True to serialize
        all related books. Setting read_only=True means books can be
        viewed but not created/updated through this serializer.
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count']
        read_only_fields = ['id', 'books', 'book_count']
    
    def validate_name(self, value):
        """
        Validate the author's name.
        
        Args:
            value (str): The author's name to validate
            
        Returns:
            str: The validated name
        """
        # Ensure name is not just whitespace
        if not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        return value.strip()
