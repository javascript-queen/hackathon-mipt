from django.db import models

from .doc import Doc


class Comparison(models.Model):
    requirements = models.ForeignKey(Doc, related_name='comparisons', on_delete=models.CASCADE)
    application = models.ForeignKey(Doc, related_name='+', on_delete=models.CASCADE)
    results = models.TextField()

    class Meta:
        unique_together = [
            ['requirements', 'application']
        ]
