from rest_framework import serializers

from main.models import Doc, User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # also see https://www.django-rest-framework.org/api-guide/relations/

    # todo prevent deletion of user objects etc (any other serializers susceptible to this problem?)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'docs']
        read_only_fields = ['username', 'email', 'docs']
