from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    
    # Book endpoints with required view names
    path('books/', views.ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='book-detail'),
    path('books/create/', views.CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.DeleteView.as_view(), name='book-delete'),
    
    # Author endpoints
    path('authors/', views.AuthorListCreate.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
]
