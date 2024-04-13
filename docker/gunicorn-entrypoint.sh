#!/bin/sh -e


cd /app
source venv/bin/activate
cd gn
mkdir -p /files/data
python manage.py migrate --noinput
rm -rf /files/data/static
python manage.py collectstatic --noinput
gunicorn --config /app/gunicorn.conf.py \
    --chdir "/app/gn" \
    "gn.asgi:application"
