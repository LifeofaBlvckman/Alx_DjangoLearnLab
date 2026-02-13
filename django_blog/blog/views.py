from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import RegisterForm, UserUpdateForm

# Home page view
def home(request):
    """
    Home page view - displays recent blog posts
    """
    posts = Post.objects.all()[:5]  # Get 5 most recent posts
    context = {
        'posts': posts,
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)

# Post detail view
def post_detail(request, pk):
    """
    Individual post view
    """
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
        'title': post.title
    }
    return render(request, 'blog/post_detail.html', context)

# ========== AUTHENTICATION VIEWS ==========

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the blog.')
            return redirect('blog-home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            # Redirect to next page if provided
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('blog-home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html', {'title': 'Login'})

def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog-home')

@login_required
def profile_view(request):
    """
    User profile view - view and edit profile
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Profile'
    }
    return render(request, 'blog/profile.html', context)

# Class-based views (alternative)
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
