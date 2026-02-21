#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements-prod.txt

# Run migrations
python manage.py migrate --settings=social_media_api.settings_production

# Collect static files
python manage.py collectstatic --no-input --settings=social_media_api.settings_production

# Create superuser if needed (optional - you can do this manually)
# python manage.py createsuperuser --noinput --settings=social_media_api.settings_production
