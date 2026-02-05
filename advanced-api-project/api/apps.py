"""
App configuration for the API application.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the API application.
    
    This class defines application-specific settings and behaviors.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """
        Method called when the app is ready.
        
        This can be used for signal registration or other startup tasks.
        """
        pass
