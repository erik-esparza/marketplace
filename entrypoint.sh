#!/bin/sh
set -e  # Exit immediately if any command fails
echo "DB_HOST is '$DB_HOST'"
echo "DB_PORT is '$DB_PORT'"

# Optional: Wait for PostgreSQL to be ready
# You can install `netcat` (nc) in your image to do this
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "Database is up!"

# Run migrations
echo "Running database migrations..."
flask db upgrade # This is a migration. It is especially important to know that migrations depends on some secrets, so you must be sure they're either available as docker secrets or runtime variables.

# Check environment and run app accordingly
if [ "$FLASK_ENV" = "production" ]; then
  echo "Starting Gunicorn server..."
  exec gunicorn -b 0.0.0.0:5000 -w 4 market:app
else
  echo "Starting Flask development server..."
  exec python run.py
fi