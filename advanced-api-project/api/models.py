"""
Models for the API application.

This module defines the data models for the advanced API project,
demonstrating complex relationships and data structures.
"""

from django.db import models


class Author(models.Model):
    """
    Author Model
    
    Represents an author who can write multiple books.
    This model demonstrates a simple entity with a one-to-many relationship.
    
    Attributes:
        name (CharField): The name of the author with a maximum length of 100 characters.
                          This field is required and should be unique to avoid duplicates.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The full name of the author")
    
    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        """
        String representation of the Author model.
        
        Returns:
            str: The author's name
        """
        return self.name
    
    def book_count(self):
        """
        Helper method to get the number of books by this author.
        
        Returns:
            int: Number of books written by this author
        """
        return self.books.count()


class Book(models.Model):
    """
    Book Model
    
    Represents a book written by an author. This model demonstrates
    a foreign key relationship and includes validation for publication year.
    
    Attributes:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author model establishing a
                            one-to-many relationship (one author, many books)
    """
    title = models.CharField(
        max_length=200, 
        help_text="The complete title of the book"
    )
    publication_year = models.IntegerField(
        help_text="The year when the book was first published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # Cascade delete: if author is deleted, delete their books
        related_name='books',      # Allows reverse lookup: author.books.all()
        help_text="The author who wrote this book"
    )
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        """
        String representation of the Book model.
        
        Returns:
            str: Book title and publication year
        """
        return f"{self.title} ({self.publication_year})"
