# Create Operation

## Command
```python
from bookshelf.models import Book

# Create a new Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(f"Created: {book}")
```

## Expected Output
```
Created: 1984 by George Orwell (1949)
```

## Notes
- Creates and saves a new Book record in the database.
- Returns the created Book instance.
