import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("\nCreating test users...")

# Delete existing test users
test_usernames = ['admin_user', 'librarian_user', 'member_user', 'regular_user'] 
User.objects.filter(username__in=test_usernames).delete()

# Create Admin user
admin_user = User.objects.create_user(
    username='admin_user',
    email='admin@example.com',
    password='admin123'
)
# Update the auto-created profile with Admin role
admin_user.user_profile.role = 'Admin'
admin_user.user_profile.save()
print(f"✓ Created Admin user: {admin_user.username} (password: admin123)")

# Create Librarian user
librarian_user = User.objects.create_user(
    username='librarian_user',
    email='librarian@example.com',
    password='librarian123'
)
# Update the auto-created profile with Librarian role
librarian_user.user_profile.role = 'Librarian'
librarian_user.user_profile.save()
print(f"✓ Created Librarian user: {librarian_user.username} (password: librarian123)")

# Create Member user
member_user = User.objects.create_user(
    username='member_user',
    email='member@example.com',
    password='member123'
)
# Update the auto-created profile with Member role
member_user.user_profile.role = 'Member'
member_user.user_profile.save()
print(f"✓ Created Member user: {member_user.username} (password: member123)")

# Create regular user
regular_user = User.objects.create_user(
    username='regular_user',
    email='regular@example.com',
    password='regular123'
)
# Update the auto-created profile with Member role
regular_user.user_profile.role = 'Member'
regular_user.user_profile.save()
print(f"✓ Created Regular user: {regular_user.username} (password: regular123)") 

print("\n✓ All test users recreated successfully!")

# Verify the users were created correctly
print("\nVerifying user profiles:")
for username in test_usernames:
    user = User.objects.get(username=username)
    print(f"  - {username}: {user.user_profile.role}")
