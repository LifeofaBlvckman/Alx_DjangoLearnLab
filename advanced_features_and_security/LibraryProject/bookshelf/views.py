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

# ALX Requirement: View using ExampleForm
from .forms import ExampleForm, SearchForm

def example_form_view(request):
    """Example view demonstrating secure form handling"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # ALX Security: Form is validated and sanitized
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # In a real application, you would save to database here
            # Using Django ORM prevents SQL injection
            
            return render(request, 'bookshelf/form_success.html', {
                'name': name,
                'form': ExampleForm()  # Return empty form for new submission
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})


def secure_search_view(request):
    """Demonstrate secure search with form validation"""
    results = []
    query = ''
    
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # ALX Security: Using Django ORM prevents SQL injection
            if query:
                results = Book.objects.filter(
                    models.Q(title__icontains=query) |
                    models.Q(author__icontains=query)
                )
    else:
        form = SearchForm()
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': query,
    })
