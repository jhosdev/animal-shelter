#!/bin/sh

if [ -f /app/.env ]; then
    export $(cat /app/.env | xargs)
fi

# Change to the app directory
cd /app/backend

# Apply database migrations
echo "Applying database migrations"
python manage.py makemigrations
python manage.py migrate --noinput

# Start the server using gunicorn
echo "Starting the server"
gunicorn backend.wsgi:application --bind 0.0.0.0:8000

# command docker run -dp 127.0.0.1:8000:8000 <container>