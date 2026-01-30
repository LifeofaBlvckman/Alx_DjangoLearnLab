#!/bin/bash
echo "Setting up LibraryProject..."
cd "$(dirname "$0")"

# Install requirements
pip install -r requirements.txt 2>/dev/null || echo "Installing Django and django-csp..."

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo "Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Run security test
echo "Running security tests..."
python test_security.py

# Run server
echo "Starting development server..."
echo "Visit: http://127.0.0.1:8000/"
python manage.py runserver
