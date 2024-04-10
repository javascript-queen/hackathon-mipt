from django.core.validators import FileExtensionValidator, ValidationError
from rest_framework import serializers


class DrfFileExtensionValidator:
    def __init__(self, allowed_extensions: list):
        self.django_validator = FileExtensionValidator(allowed_extensions)

    def __call__(self, value):
        try:
            self.django_validator(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.message % exc.params)
