import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User

# Create test users with different roles
users_data = [
    {'username': 'admin_user', 'email': 'admin@example.com', 'password': 'password123', 'role': 'Admin'},
    {'username': 'librarian_user', 'email': 'librarian@example.com', 'password': 'password123', 'role': 'Librarian'},
    {'username': 'member_user', 'email': 'member@example.com', 'password': 'password123', 'role': 'Member'},
]

print("Creating test users...")

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={'email': user_data['email']}
    )
    
    if created:
        user.set_password(user_data['password'])
        user.save()
        # The profile should be created automatically by the signal
        user.profile.role = user_data['role']
        user.profile.save()
        print(f"✓ Created user: {user_data['username']} with role: {user_data['role']}")
    else:
        # Update existing user's role
        user.profile.role = user_data['role']
        user.profile.save()
        print(f"✓ Updated user: {user_data['username']} with role: {user_data['role']}")

print("\n" + "="*50)
print("Test users created successfully!")
print("="*50)
print("\nLogin credentials:")
print("-" * 30)
print("Admin:      admin_user / password123")
print("Librarian:  librarian_user / password123")
print("Member:     member_user / password123")
print("\nAccess URLs:")
print("-" * 30)
print("Admin View:      http://127.0.0.1:8000/admin-view/")
print("Librarian View:  http://127.0.0.1:8000/librarian-view/")
print("Member View:     http://127.0.0.1:8000/member-view/")
print("Django Admin:    http://127.0.0.1:8000/admin/")
