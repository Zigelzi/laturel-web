#!/bin/sh

if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting development container!"
fi

# Skip this for now
# TODO: Figure out how to set up dev DB with mockup data
# python manage.py create_db

exec "$@"
