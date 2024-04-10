from .base_viewsets import AbstractAuthViewSet
from main.models import User
from main.serializers import UserSerializer


class UserViewSet(AbstractAuthViewSet):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'current':
            return self.request.user

        return super().get_object()
