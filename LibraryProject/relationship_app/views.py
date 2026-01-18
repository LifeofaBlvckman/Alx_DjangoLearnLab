from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Library, UserProfile

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    from .models import Book
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimize query by prefetching related books and their authors
        return Library.objects.prefetch_related('books__author')

# Registration view (function-based) - Updated to set default role
def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful! You have been assigned the Member role.')
            return redirect('list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Custom Login View using Django's LoginView
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('list_books')

# Custom Logout View using Django's LogoutView
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)

# Role check functions for user_passes_test decorator
def admin_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin()

def librarian_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_librarian()

def member_required(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_member()

# Role-Based Views

@login_required
@user_passes_test(admin_required, login_url='/login/')
def admin_view(request):
    """
    View accessible only to users with Admin role.
    """
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.profile.role if hasattr(request.user, 'profile') else 'No role assigned'
    })

@login_required
@user_passes_test(librarian_required, login_url='/login/')
def librarian_view(request):
    """
    View accessible only to users with Librarian role.
    """
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.profile.role if hasattr(request.user, 'profile') else 'No role assigned'
    })

@login_required
@user_passes_test(member_required, login_url='/login/')
def member_view(request):
    """
    View accessible only to users with Member role.
    """
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.profile.role if hasattr(request.user, 'profile') else 'No role assigned'
    })
