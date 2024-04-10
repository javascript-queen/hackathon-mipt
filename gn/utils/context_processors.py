from django.conf import settings
from django.urls import reverse

from main.serializers import UserSerializer


def custom_processor(request):
    class SafeSettings:
        DEBUG = settings.DEBUG
        LOCAL = settings.LOCAL
        VITE_SERVER_BASE_URL = settings.VITE_SERVER_BASE_URL

    current_user_data = None
    if not request.user.is_anonymous:
        current_user_data = UserSerializer(request.user, context=dict(request=request)).data

    return dict(
        settings=SafeSettings,
        base_js_data=dict(
            docs_endpoint=reverse('doc-list'),
            files_endpoint=reverse('file-list'),
            users_endpoint=reverse('user-list'),
            current_user=current_user_data,
        ),
        js_data='{}',
    )
