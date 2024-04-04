from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'main'
    verbose_name = 'main'

    def ready(self):
        post_migrate.connect(_create_demo_user, sender=self)


def _create_demo_user(**kwargs):
    from main.models import User
    username = 'demo'
    exists = User.objects.filter(username=username).exists()
    if not exists:
        User.objects.create_user(username, 'demo@example.com', password='demo')
