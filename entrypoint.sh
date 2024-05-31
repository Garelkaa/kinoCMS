#!/bin/bash

# Apply migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from users.models import CustomUser; CustomUser.objects.filter(email='admin@example.com').count() or CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Run your database initialization scripts
python fill_table.py

# Start the Django development server
exec "$@"
