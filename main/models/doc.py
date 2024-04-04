from django.db import models

from .user import User


class Doc(models.Model):
    user = models.ForeignKey(User, related_name='docs', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
