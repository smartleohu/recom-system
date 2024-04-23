#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h $DB_HOST -p $DB_PORT >/dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is ready."

# Apply Django database migrations
echo "Applying Django database migrations..."
python manage.py migrate

# Collect static files (if applicable)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Elasticsearch (if applicable)
echo "Starting Elasticsearch..."
elasticsearch-full &

# Start Celery worker
echo "Starting Celery worker..."
celery -A recom_system worker -l info &

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn recom_system.app.wsgi:application --bind 0.0.0.0:$PORT --workers $GUNICORN_WORKERS
