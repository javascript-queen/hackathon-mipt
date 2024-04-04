from rest_framework import serializers

from main.models import Doc


class DocSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Doc
        fields = ['id', 'user', 'name']
