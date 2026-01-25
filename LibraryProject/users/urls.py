from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Role-based views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
