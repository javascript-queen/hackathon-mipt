from pathlib import Path
import tempfile

from django.core.files import File as DjangoFile
from django.core.files.storage import FileSystemStorage as DjangoFileSystemStorage


class FileSystemStorage(DjangoFileSystemStorage):
    def path(self, name):
        return super().path(self._calc_in_storage_path(name))

    def url(self, name):
        return super().url(self._calc_in_storage_path(name))

    def save(self, name, content, max_length=None):
        if not hasattr(content, 'chunks'):
            content = DjangoFile(content)
        with tempfile.TemporaryDirectory(dir=super().path('tmp')) as tmp_dir:
            length = 0
            with Path(tmp_dir).joinpath(name).open('wb') as tmp_fh:
                for chunk in content.chunks(8192):
                    length += len(chunk)
                    tmp_fh.write(chunk)
                    if max_length is not None and length > max_length:
                        break
                super().save(name, _TempFile(tmp_fh, name=name), max_length=max_length)
        return name

    @staticmethod
    def _calc_in_storage_path(name):
        name = name.lower()
        return f'{name[:2]}/{name[2:4]}/{name}'


class _TempFile(DjangoFile):
    def temporary_file_path(self):
        return self.file.name
