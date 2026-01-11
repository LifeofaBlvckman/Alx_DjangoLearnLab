# Django ORM CRUD Operations for Book Model

## 1. Create
```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(book)
```
**Output:** `1984 by George Orwell (1949)`

## 2. Retrieve
```python
book = Book.objects.get(title="1984")
print(f"{book.title}, {book.author}, {book.publication_year}")
```
**Output:** `1984, George Orwell, 1949`

## 3. Update
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```
**Output:** `Nineteen Eighty-Four`

## 4. Delete
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all().count())
```
**Output:** `0`

## Summary
Successfully implemented all CRUD operations.
