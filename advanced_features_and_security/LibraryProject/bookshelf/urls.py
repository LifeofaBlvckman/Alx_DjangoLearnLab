from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('example/', views.example_form_view, name='example_form'),
    path('search/', views.secure_search_view, name='secure_search'),
]
