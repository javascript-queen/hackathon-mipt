from rest_framework import serializers

from main.models import File


class FileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'file', 'docs']
