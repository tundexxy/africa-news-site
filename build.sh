#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Apply any outstanding database migrations
# This ensures your database schema is up-to-date on Render
python manage.py migrate

# Collect static asset files (CSS, JS, images)
# --no-input means it won't ask for confirmation
python manage.py collectstatic --no-input