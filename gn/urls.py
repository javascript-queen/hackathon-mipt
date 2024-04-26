"""
URL configuration for gn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static as urls_static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from main import api

admin.site.site_header = settings.ADMIN_SITE_HEADER

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', api.UserViewSet)
router.register('comparisons', api.ComparisonViewSet)
router.register('docs', api.DocViewSet)
router.register('files', api.FileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # login, logout
    path('login', auth_views.LoginView.as_view(next_page='admin'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),

    path('', include('main.urls', namespace='main')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))


if settings.LOCAL and settings.DEBUG:
    urlpatterns += urls_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # serve favicon (remove annoying console errors)
    from django.views import static
    urlpatterns += [
        path(r'favicon.ico',
             static.serve,
             dict(document_root=Path(__file__).parent.joinpath('static', 'images', 'icons'),
                  path='favicon.ico'))
    ]
