# Django ORM CRUD Operations for Book Model

## CREATE Operation
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

**Output:**
```
<Book: 1984 by George Orwell (1949)>
```

## RETRIEVE Operation
```python
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

**Output:**
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## UPDATE Operation
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

**Output:**
```
Updated title: Nineteen Eighty-Four
```

## DELETE Operation
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Confirm deletion
all_books = Book.objects.all()
print(f"Books in database: {all_books}")
```

**Output:**
```
Books in database: <QuerySet []>
```
