import os
import sys
import django

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
try:
    django.setup()
    
    from django.urls import reverse, resolve
    
    print("Testing URL patterns...")
    
    # Test if we can resolve URLs
    try:
        url = reverse('home')
        print(f"✓ Home URL: {url}")
    except Exception as e:
        print(f"✗ Home URL error: {e}")
    
    try:
        url = reverse('admin_view')
        print(f"✓ Admin view URL: {url}")
    except Exception as e:
        print(f"✗ Admin view URL error: {e}")
    
    try:
        url = reverse('login')
        print(f"✓ Login URL: {url}")
    except Exception as e:
        print(f"✗ Login URL error: {e}")
        
except Exception as e:
    print(f"Setup error: {e}")
