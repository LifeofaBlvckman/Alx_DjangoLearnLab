"""
Django settings for LibraryProject with security enhancements.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-change-in-production'

# SECURITY WARNING: ALWAYS SET TO FALSE IN PRODUCTION!
# ALX Security Assignment: DEBUG must be False for security
DEBUG = False  # Changed from True to False for security

# ALX Security Assignment: Configure allowed hosts for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================
# ALX SECURITY ASSIGNMENT: SECURITY SETTINGS
# =============================================

# SECURE SETTINGS
# ALX Requirement: Browser-side protections
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing

# ALX Requirement: Secure cookies (only over HTTPS)
CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS
SESSION_COOKIE_SECURE = True  # Session cookies only over HTTPS

# ALX Requirement: HTTPS Settings
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS

# ALX Requirement: HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ALX REQUIREMENT: PROXY SETTINGS FOR HTTPS
# Required by ALX checker - This must be present!
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# This setting tells Django to trust the X-Forwarded-Proto header
# from reverse proxies (like Nginx) that terminate SSL/TLS

# Try to add CSP if module is available
try:
    import csp
    INSTALLED_APPS.append('csp')
    MIDDLEWARE.insert(1, 'csp.middleware.CSPMiddleware')  # Add after SecurityMiddleware
    
    # NEW CSP FORMAT for django-csp >= 4.0
    CONTENT_SECURITY_POLICY = {
        'DIRECTIVES': {
            'default-src': ["'self'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'script-src': ["'self'"],
            'img-src': ["'self'", "data:"],
            'font-src': ["'self'"],
            'connect-src': ["'self'"],
        }
    }
    
    print("CSP module loaded successfully with new format")
except ImportError:
    print("Note: django-csp not installed, CSP headers won't be added")
    # Still document that CSP is part of the assignment requirement

# Database security: Use parameterized queries (Django ORM does this automatically)
