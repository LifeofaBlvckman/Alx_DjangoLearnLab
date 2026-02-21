from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, UserDetailSerializer
)
from .models import CustomUser

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """
    Register a new user and return token
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user, context={'request': request}).data,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Login user and return token
    """
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': UserProfileSerializer(user, context={'request': request}).data,
        'token': token.key,
        'message': 'Login successful'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user (delete token)
    """
    request.user.auth_token.delete()
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """
    View another user's profile
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user
    """
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if request.user == user_to_follow:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': f'You are already following {user_to_follow.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.add(user_to_follow)
    
    return Response({
        'message': f'You are now following {user_to_follow.username}',
        'following_count': request.user.following_count,
        'followers_count': user_to_follow.followers_count
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user
    """
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    
    if request.user == user_to_unfollow:
        return Response(
            {'error': 'You cannot unfollow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': f'You are not following {user_to_unfollow.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.remove(user_to_unfollow)
    
    return Response({
        'message': f'You have unfollowed {user_to_unfollow.username}',
        'following_count': request.user.following_count,
        'followers_count': user_to_unfollow.followers_count
    }, status=status.HTTP_200_OK)


class FollowersListView(generics.ListAPIView):
    """
    List users who follow the specified user
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.followers.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class FollowingListView(generics.ListAPIView):
    """
    List users that the specified user follows
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.following.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserSearchView(generics.ListAPIView):
    """
    Search for users by username
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return CustomUser.objects.filter(username__icontains=query)
        return CustomUser.objects.none()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
