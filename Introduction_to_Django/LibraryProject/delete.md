# Delete Operation
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Confirm deletion
Book.objects.all()
```

**Expected Output:**
```
<QuerySet []>
```
