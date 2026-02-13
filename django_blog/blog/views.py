from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import RegisterForm, UserUpdateForm, PostForm

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


# ========== BLOG POST CRUD VIEWS ==========

class PostListView(ListView):
    """
    Display all blog posts
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog Posts'
        return context


class PostDetailView(DetailView):
    """
    Display individual blog post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post (authenticated users only)
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a blog post (only author can update)
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Show success message
        """
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context
    
    def test_func(self):
        """
        Check if the current user is the author of the post
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post (only author can delete)
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    context_object_name = 'post'
    
    def delete(self, request, *args, **kwargs):
        """
        Show success message on delete
        """
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context
    
    def test_func(self):
        """
        Check if the current user is the author of the post
        """
        post = self.get_object()
        return self.request.user == post.author


# Legacy function-based views for backward compatibility
def home(request):
    """
    Home page view - redirects to post list
    """
    return redirect('post-list')

def post_detail(request, pk):
    """
    Legacy post detail view
    """
    return PostDetailView.as_view()(request, pk=pk)
