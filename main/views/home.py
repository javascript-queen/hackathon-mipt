import logging

from django.shortcuts import render
from django.views import View

from main.models import User


class HomeView(View):

    def get(self, request):
        logger = logging.getLogger('django')

        logger.error('exemplary home view error log message')
        logger.debug('exemplary home view debug log message')

        context = dict(
            js_data=dict(
                message='Hello World!',
                user_count=User.objects.count(),
            ),
        )

        return render(request, 'main/home.html', context)
