from django.db import models


class FileField(models.FileField):
    """
    Disregards the storage kwarg when creating migrations for this field
    """
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop('storage', None)
        return name, path, args, kwargs
