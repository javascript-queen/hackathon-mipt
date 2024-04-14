from rest_framework import serializers

from .base import HyperlinkedModelSerializer
from ..models import Comparison


class ComparisonSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Comparison
        fields = ['id', 'url', 'requirements', 'application', 'results']
        read_only_fields = ['results']
        no_update_fields = ['requirements', 'application']

    def validate(self, data: dict):
        requirements = data.get('requirements')
        application = data.get('application')
        errors = {}

        # Ensure one doc - requirements, the other - application.
        if not requirements.is_requirements:
            errors['requirements'] = f"Документ {requirements.id} - не требования, а заявка."
        if application.is_requirements:
            errors['application'] = f"Документ {application.id} - не заявка, а требования."

        # Ensure both docs belong to the same user
        if application.user.id == requirements.user.id:
            # note: ['error msg1', ...] is also ok
            errors['non_field_errors'] = f'Документы принадлежат разным пользователям.'

        if errors:
            raise serializers.ValidationError(errors)

        return data
