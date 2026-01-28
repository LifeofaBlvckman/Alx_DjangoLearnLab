from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Article URLs
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:pk>/publish/', views.article_publish, name='article_publish'),
    
    # Comment URLs
    path('article/<int:article_pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
