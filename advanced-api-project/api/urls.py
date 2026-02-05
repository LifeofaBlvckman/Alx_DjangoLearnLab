"""
URL configuration for the API application.

This module defines the URL patterns for the API endpoints,
mapping URLs to their corresponding views.
"""

from django.urls import path
from . import views

# URL patterns for the API application
urlpatterns = [
    # Root endpoint
    path('', views.api_root, name='api-root'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreate.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    
    # Book endpoints
    path('books/', views.BookListCreate.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
]
