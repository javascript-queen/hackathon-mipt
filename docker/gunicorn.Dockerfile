

# todo fix hash
FROM python:3.12.3-alpine3.19

WORKDIR /app

COPY gn gn

RUN apk add --no-cache --virtual .build-deps g++ gcc libc-dev libxslt-dev \
    && apk add --no-cache libxslt libstdc++ \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir poetry \
    && python -m venv venv \
    && . venv/bin/activate \
    && cd gn \
    && poetry install --no-cache \
    && poetry add --no-cache gunicorn uvicorn \
    && apk del .build-deps

ENTRYPOINT ["docker-entrypoint.sh"]
