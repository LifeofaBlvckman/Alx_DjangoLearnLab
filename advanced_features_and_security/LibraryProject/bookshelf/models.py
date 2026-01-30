from django.db import models

class Book(models.Model):
    """Book model for LibraryProject"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    description = models.TextField()
    
    # ALX Security: Using Django ORM prevents SQL injection
    
    def __str__(self):
        return f"{self.title} by {self.author}"
