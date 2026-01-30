from django.db import models
from django.conf import settings
from django.utils import timezone


class Article(models.Model):
    """Example model with custom permissions for the assignment"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='articles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        # Order by newest first by default
        ordering = ['-created_at']
        # Custom permissions as specified in the assignment
        permissions = [
            ("can_view", "Can view article"),
            ("can_create", "Can create article"),
            ("can_edit", "Can edit article"),
            ("can_delete", "Can delete article"),
            ("can_publish", "Can publish article"),
        ]
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """Another model with custom permissions for demonstration"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        permissions = [
            ("can_view", "Can view comment"),
            ("can_create", "Can create comment"),
            ("can_edit", "Can edit comment"),
            ("can_delete", "Can delete comment"),
        ]
    
    def __str__(self):
        return f"Comment by {self.user.email} on {self.article.title}"
