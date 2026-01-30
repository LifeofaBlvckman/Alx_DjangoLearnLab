# Delete Operation

## Command
```python
from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
count = Book.objects.all().count()
print(f"Books in database: {count}")
```

## Expected Output
```
Books in database: 0
```

## Notes
- Permanently removes the record.
- Confirm with count() method.
