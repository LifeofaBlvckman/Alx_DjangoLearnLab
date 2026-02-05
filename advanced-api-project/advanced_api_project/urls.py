"""
Main URL configuration for the advanced_api_project.

This module routes URLs to the appropriate applications.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
]
