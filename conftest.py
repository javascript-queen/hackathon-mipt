import os
import django

# This is pytest config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')


def pytest_configure():
    django.setup()
