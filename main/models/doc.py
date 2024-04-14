from django.db import models

from .file import File
from .user import User


class Doc(models.Model):
    user = models.ForeignKey(User, related_name='docs', on_delete=models.CASCADE)
    file = models.ForeignKey(File, related_name='docs', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    # todo impl validation related to the 'no more than 1 requirement per project' constraint and validation
    is_requirements = models.BooleanField()

    class Meta:
        unique_together = [
            # todo impl validation related to this constraint in serializer
            ['user', 'file', 'is_requirements']
        ]
