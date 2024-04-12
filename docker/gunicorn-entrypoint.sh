#!/bin/sh -e


# todo refactor to docker config
cd /app
. venv/bin/activate
cd gn
python manage.py migrate
gunicorn --config /app/gunicorn.conf.py \
    --chdir "/app/gn" \
    "gn.asgi:application"
