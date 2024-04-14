import hashlib
import os

from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import serializers

from .base import HyperlinkedModelSerializer
from .validation import DrfFileExtensionValidator
from ..models import Doc, File


class DocSerializer(HyperlinkedModelSerializer):

    file = serializers.FileField(
        validators=[DrfFileExtensionValidator(['docx'])],
        allow_empty_file=False,
        max_length=10000000,  # todo to settings
    )

    class Meta:
        model = Doc
        fields = ['id', 'url', 'user', 'name', 'file', 'is_requirements']
        read_only_fields = ['user']
        no_update_fields = ['user', 'file', 'is_requirements']

    def create(self, validated_data):
        print('validated data:', validated_data)

        user = validated_data.get('user')
        file_obj = validated_data.get('file')
        name = validated_data.get('name') or file_obj.name
        is_requirements = validated_data.get('is_requirements')

        file_obj.seek(os.SEEK_SET)

        # calc filename as md5 hash of file bytes
        md5 = hashlib.md5()
        for chunk in iter(lambda: file_obj.read(8192), b''):
            md5.update(chunk)
        filename = md5.hexdigest()
        with transaction.atomic():
            file = File.objects.filter(file=filename).first()
            if settings.LOCAL:
                print(filename, 'exists', bool(file))
            if not file:
                file = File()
                try:
                    file.file.save(filename, file_obj)
                except IntegrityError:
                    file = File.objects.filter(file=filename).first()
                    if not file:
                        raise
            # todo maybe db index etc
            doc, _ = Doc.objects.get_or_create(user=user, file=file, is_requirements=is_requirements, name=name)
            # todo impl cleanup of dangling requirements (mind race conditions)
            # todo maybe extract all db-altering code to single thread
        return doc
