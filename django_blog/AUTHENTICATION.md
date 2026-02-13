# Django Blog - Authentication System Documentation

## Overview
This document describes the authentication system implemented in the Django Blog project.

## Features
1. **User Registration** - New users can create accounts
2. **User Login** - Registered users can log in
3. **User Logout** - Users can log out
4. **Profile Management** - Users can view and edit their profile

## Implementation Details

### Forms (forms.py)
- `RegisterForm`: Extends Django's UserCreationForm with email, first_name, last_name
- `UserUpdateForm`: Allows users to update their profile information

### Views (views.py)
- `register_view`: Handles new user registration
- `login_view`: Handles user authentication
- `logout_view`: Handles user logout
- `profile_view`: Displays and processes profile updates (requires login)

### Templates
- `register.html`: Registration form
- `login.html`: Login form
- `profile.html`: Profile view/edit page

### URL Patterns
- `/register/` - Registration page
- `/login/` - Login page  
- `/logout/` - Logout
- `/profile/` - Profile page (requires login)

## Testing Instructions

### Test Registration
1. Navigate to `/register/`
2. Fill in the registration form
3. Submit - should redirect to home with success message

### Test Login
1. Navigate to `/login/`
2. Enter credentials
3. Submit - should redirect to home with welcome message

### Test Profile Update
1. Log in
2. Navigate to `/profile/`
3. Update information
4. Submit - should show success message

### Test Logout
1. Click "Logout" in navigation
2. Should redirect to home with logout message

## Security Features
- CSRF tokens on all forms
- Password hashing using Django's built-in algorithms
- Login required decorator for protected views
- Session management handled by Django
