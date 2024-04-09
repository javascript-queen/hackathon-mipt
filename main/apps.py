from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'main'
    verbose_name = 'main'

    def ready(self):
        post_migrate.connect(_create_demo_users, sender=self)
        post_migrate.connect(_create_media_and_media_tmp_dir, sender=self)


def _create_demo_users(**kwargs):
    if not settings.LOCAL:
        return
    from main.models import User
    username = 'demo'
    exists = User.objects.filter(username=username).exists()
    if not exists:
        User.objects.create_user(username, 'demo@example.com', password='demo')
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')


def _create_media_and_media_tmp_dir(**kwargs):
    settings.MEDIA_ROOT.joinpath('tmp').mkdir(parents=True, exist_ok=True)
