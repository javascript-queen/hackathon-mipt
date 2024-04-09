from django.db import models

from .file import File
from .user import User


class Doc(models.Model):
    user = models.ForeignKey(User, related_name='docs', on_delete=models.CASCADE)
    file = models.ForeignKey(File, related_name='docs', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
