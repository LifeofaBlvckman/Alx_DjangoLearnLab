from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Article, Comment


# ==================== ARTICLE VIEWS ====================

@permission_required('content.can_view', raise_exception=True)
def article_list(request):
    """List all articles - requires can_view permission"""
    articles = Article.objects.all()
    return render(request, 'content/article_list.html', {
        'articles': articles,
        'can_create': request.user.has_perm('content.can_create'),
        'can_edit': request.user.has_perm('content.can_edit'),
        'can_delete': request.user.has_perm('content.can_delete'),
        'can_publish': request.user.has_perm('content.can_publish'),
    })


@permission_required('content.can_view', raise_exception=True)
def article_detail(request, pk):
    """View single article - requires can_view permission"""
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()
    
    context = {
        'article': article,
        'comments': comments,
        'can_edit': request.user.has_perm('content.can_edit'),
        'can_delete': request.user.has_perm('content.can_delete'),
        'can_create_comment': request.user.has_perm('content.can_create'),
    }
    return render(request, 'content/article_detail.html', context)


@login_required
@permission_required('content.can_create', raise_exception=True)
def article_create(request):
    """Create new article - requires can_create permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if not title or not content:
            messages.error(request, 'Title and content are required.')
        else:
            article = Article.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, f'Article "{article.title}" created successfully!')
            return redirect('article_detail', pk=article.pk)
    
    return render(request, 'content/article_form.html', {
        'action': 'Create',
        'title': '',
        'content': '',
    })


@login_required
@permission_required('content.can_edit', raise_exception=True)
def article_edit(request, pk):
    """Edit article - requires can_edit permission"""
    article = get_object_or_404(Article, pk=pk)
    
    # Additional permission check: users can only edit their own articles unless they have special permission
    if article.author != request.user and not request.user.has_perm('content.can_edit_others'):
        raise PermissionDenied("You can only edit your own articles.")
    
    if request.method == 'POST':
        article.title = request.POST.get('title', article.title)
        article.content = request.POST.get('content', article.content)
        article.save()
        messages.success(request, f'Article "{article.title}" updated successfully!')
        return redirect('article_detail', pk=article.pk)
    
    return render(request, 'content/article_form.html', {
        'action': 'Edit',
        'title': article.title,
        'content': article.content,
    })


@login_required
@permission_required('content.can_delete', raise_exception=True)
def article_delete(request, pk):
    """Delete article - requires can_delete permission"""
    article = get_object_or_404(Article, pk=pk)
    
    if article.author != request.user and not request.user.has_perm('content.can_delete_others'):
        raise PermissionDenied("You can only delete your own articles.")
    
    if request.method == 'POST':
        title = article.title
        article.delete()
        messages.success(request, f'Article "{title}" deleted successfully!')
        return redirect('article_list')
    
    return render(request, 'content/article_confirm_delete.html', {'article': article})


@login_required
@permission_required('content.can_publish', raise_exception=True)
def article_publish(request, pk):
    """Publish/unpublish article - requires can_publish permission"""
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        article.is_published = not article.is_published
        article.save()
        status = "published" if article.is_published else "unpublished"
        messages.success(request, f'Article "{article.title}" {status} successfully!')
    
    return redirect('article_detail', pk=article.pk)


# ==================== COMMENT VIEWS ====================

@permission_required('content.can_create', raise_exception=True)
def comment_create(request, article_pk):
    """Create comment - requires can_create permission for comments"""
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(
                article=article,
                user=request.user,
                text=text
            )
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment text cannot be empty.')
    
    return redirect('article_detail', pk=article_pk)


@login_required
@permission_required('content.can_delete', raise_exception=True)
def comment_delete(request, pk):
    """Delete comment - requires can_delete permission for comments"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Users can delete their own comments or comments on their articles
    can_delete = (
        comment.user == request.user or 
        comment.article.author == request.user or
        request.user.has_perm('content.can_delete_others')
    )
    
    if not can_delete:
        return HttpResponseForbidden("You don't have permission to delete this comment.")
    
    article_pk = comment.article.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('article_detail', pk=article_pk)

# ALX Assignment: Permission-protected views
# All views use @permission_required decorators
# Testing: See test_alx_assignment.py
