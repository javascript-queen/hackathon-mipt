from .base_viewsets import AbstractAuthViewSet
from main.models import User
from main.serializers import UserSerializer


class UserViewSet(AbstractAuthViewSet):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
