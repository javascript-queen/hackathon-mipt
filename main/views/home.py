import json
import logging

from django.shortcuts import render
from django.urls import reverse
from django.views import View

from main.models import User


class HomeView(View):

    def get(self, request):
        logger = logging.getLogger('django')

        logger.error('exemplary home view error log message')
        logger.debug('exemplary home view debug log message')

        context = dict(
            # todo auto merge with gn.utils.context_processors
            js_data=json.dumps(dict(
                message='Hello World!',
                user_count=User.objects.count(),
                # todo refactor extract to gn.utils.context_processors
                docs_endpoint=reverse('doc-list'),
                users_endpoint=reverse('user-list'),
            ),
        ))

        return render(request, 'main/home.html', context)
