from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post

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
