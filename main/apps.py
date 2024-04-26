from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'main'
    verbose_name = 'main'

    def ready(self):
        post_migrate.connect(_create_demo_users, sender=self)
        post_migrate.connect(_create_data_dirs, sender=self)


def _create_demo_users(**kwargs):
    from main.models import User
    username = 'demo'
    exists = User.objects.filter(username=username).exists()
    if not exists:
        User.objects.create_user(username, 'demo@example.com', password='demo')
    if not settings.LOCAL:
        return
    username = 'admin'
    exists = User.objects.filter(username=username).exists()
    if not exists:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


def _create_data_dirs(**kwargs):
    settings.DATA_ROOT.joinpath('media', 'tmp').mkdir(parents=True, exist_ok=True)
