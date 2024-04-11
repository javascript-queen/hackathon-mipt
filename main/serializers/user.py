from rest_framework import serializers

from main.models import Doc, User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # also see https://www.django-rest-framework.org/api-guide/relations/

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'docs']
