#!/usr/bin/python3
import os

print("=== Current Directory ===")
print(os.getcwd())
print()

print("=== Files in Current Directory ===")
os.system("ls -la *.md")
print()

print("=== Bookshelf App Files ===")
os.system("find bookshelf -name '*.py' | head -10")
print()

print("=== Book Model Check ===")
if os.path.exists("bookshelf/models.py"):
    with open("bookshelf/models.py", 'r') as f:
        content = f.read()
        checks = [
            ("Book model class", 'class Book(models.Model):'),
            ("title field", 'title = models.CharField(max_length=200)'),
            ("author field", 'author = models.CharField(max_length=100)'),
            ("publication_year field", 'publication_year = models.IntegerField()')
        ]
        
        for check_name, check_str in checks:
            if check_str in content:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
else:
    print("❌ bookshelf/models.py not found")
