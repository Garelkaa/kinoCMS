#!/bin/bash

# Apply migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').count() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Run your database initialization scripts
python fill_table.py

# Start the Django development server
exec "$@"
