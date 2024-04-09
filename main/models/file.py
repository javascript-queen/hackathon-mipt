from pathlib import Path

from django.conf import settings
from django.db import models

from .utils.file_field import FileField
from .utils.file_system_storage import FileSystemStorage


storage = FileSystemStorage(location=settings.MEDIA_ROOT)


class File(models.Model):

    file = FileField(unique=True, storage=storage)

    @property
    def path(self):
        return Path(self.file.storage.path(self.file.name))

    @property
    def url(self):
        return self.file.storage.url(self.file.name)
