# Update Operation

## Command
```python
from bookshelf.models import Book

# Retrieve and update
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated to: {book.title}")
```

## Expected Output
```
Updated to: Nineteen Eighty-Four
```

## Notes
- Modifies an existing record.
- Must call save() to persist changes.
