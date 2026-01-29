# ALX Django Permissions Assignment

## Step 1: Custom Permissions in models.py

Article model:
class Meta:
    permissions = [
        ("can_view", "Can view article"),
        ("can_create", "Can create article"),
        ("can_edit", "Can edit article"),
        ("can_delete", "Can delete article"),
        ("can_publish", "Can publish article"),
    ]

Comment model:
class Meta:
    permissions = [
        ("can_view", "Can view comment"),
        ("can_create", "Can create comment"),
        ("can_edit", "Can edit comment"),
        ("can_delete", "Can delete comment"),
    ]

## Step 2: Groups in setup_groups.py
- Viewers: can_view only
- Editors: can_view, can_create, can_edit, can_delete
- Admins: All permissions including can_publish

## Step 3: Views protected in views.py
All views use @permission_required decorators.

## Step 4: Testing
Run: python manage.py setup_groups
Create test users and assign to groups.

## Step 5: Documentation
This file documents the setup.
