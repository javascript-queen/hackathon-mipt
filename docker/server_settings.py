from pathlib import Path

LOCAL = False
DEBUG = False

# todo
ALLOWED_HOSTS = ['*']

DATA_ROOT = Path('/files', 'data')
STATIC_ROOT = DATA_ROOT.joinpath('static')
DATA_TMP_ROOT = DATA_ROOT.joinpath('tmp')
MEDIA_ROOT = DATA_ROOT.joinpath('media')
MEDIA_TMP_ROOT = DATA_ROOT.joinpath('tmp')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(DATA_ROOT.joinpath('db.sqlite3')),
    }
}
