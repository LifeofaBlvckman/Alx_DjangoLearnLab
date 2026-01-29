from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm

# ALX Security: Safe view using Django ORM (prevents SQL injection)
def book_list(request):
    """Display list of books with safe search functionality"""
    query = request.GET.get('q', '').strip()
    
    # ALX Security: Using Django ORM with parameterized queries
    # This prevents SQL injection attacks
    if query:
        # Safe ORM query - no string concatenation
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    else:
        books = Book.objects.all()
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'query': query,
    })

# ALX Security: Using Django Forms for validation and CSRF protection
@login_required
def add_book(request):
    """Add a new book using Django Form for validation"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # ALX Security: Form validation prevents malicious input
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

# ALX Security: Using get_object_or_404 for safe object retrieval
def book_detail(request, pk):
    """View book details safely"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# ALX Security: Example of dangerous practice (COMMENTED OUT)
# def dangerous_search(request):
#     """DANGEROUS: Vulnerable to SQL injection - DO NOT USE"""
#     query = request.GET.get('q', '')
#     # NEVER DO THIS: Direct string interpolation in SQL
#     books = Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'")
#     return render(request, 'bookshelf/book_list.html', {'books': books})
