# This app doesn't define its own UserProfile model
# It imports from relationship_app to avoid conflicts
from relationship_app.models import UserProfile

__all__ = ['UserProfile']
