from pathlib import Path

LOCAL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}

# todo
ALLOWED_HOSTS = ['*']

MEDIA_ROOT = Path('/files/data').joinpath('media')
