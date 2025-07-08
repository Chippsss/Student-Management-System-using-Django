#!/bin/bash
# wait_for_db.sh

# Get database host and port from environment variables, fallback to defaults
DB_HOST=${POSTGRES_HOST:-db}
DB_PORT=${POSTGRES_PORT:-5432}

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Loop until the database is reachable
while ! nc -z $DB_HOST $DB_PORT; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1 # Wait for 1 second before retrying
done

echo "PostgreSQL is up - executing command"
# Execute the rest of the command passed to this script
exec "$@"
