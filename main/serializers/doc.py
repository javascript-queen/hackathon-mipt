import hashlib
import os

from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import serializers

from utils.validation import DrfFileExtensionValidator
from ..models import Doc, File


class DocSerializer(serializers.HyperlinkedModelSerializer):

    file = serializers.FileField(
        validators=[DrfFileExtensionValidator(['docx'])],
        allow_empty_file=False,
        max_length=10000000,  # todo to settings
    )

    class Meta:
        model = Doc
        fields = ['id', 'url', 'user', 'name', 'file']

    def create(self, validated_data):
        print('validated data:', validated_data)

        user = validated_data.get('user')
        file_obj = validated_data.get('file')
        name = validated_data.get('name') or file_obj.name

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
            doc, _ = Doc.objects.get_or_create(user=user, file=file, name=name)
        return doc
