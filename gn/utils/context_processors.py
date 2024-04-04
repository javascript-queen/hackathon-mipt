from django.conf import settings


def custom_processor(request):
    class SafeSettings:
        DEBUG = settings.DEBUG
        LOCAL = settings.LOCAL
        VITE_SERVER_BASE_URL = settings.VITE_SERVER_BASE_URL

    return dict(
        settings=SafeSettings,
    )
