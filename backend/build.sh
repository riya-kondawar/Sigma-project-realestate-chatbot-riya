#!/usr/bin/env bash
echo "Running build script..."
python manage.py collectstatic --noinput
python manage.py migrate
echo "Build completed!"