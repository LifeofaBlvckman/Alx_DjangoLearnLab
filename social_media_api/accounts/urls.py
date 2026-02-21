from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('search/', views.UserSearchView.as_view(), name='user-search'),

    # Follow/Unfollow - THESE ARE THE REQUIRED ROUTES
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),

    # Followers/Following Lists
    path('followers/<int:user_id>/', views.FollowersListView.as_view(), name='followers'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following'),
]
