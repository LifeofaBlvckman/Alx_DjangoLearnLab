from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, through='LibraryBook')
    
    def __str__(self):
        return self.name

class LibraryBook(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['library', 'book']
