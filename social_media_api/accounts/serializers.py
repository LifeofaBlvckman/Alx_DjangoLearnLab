from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .models import CustomUser

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, label="Confirm password")
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 
                  'followers_count', 'following_count', 'posts_count',
                  'date_joined', 'is_following']
        read_only_fields = ['id', 'date_joined']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer for viewing profiles
    """
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()
    is_self = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture',
                  'followers_count', 'following_count', 'posts_count',
                  'date_joined', 'last_login', 'is_following', 'is_self']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False
    
    def get_is_self(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id == obj.id
        return False
