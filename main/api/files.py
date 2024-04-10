from .base_viewsets import AbstractAuthViewSet
from main.models import File
from main.serializers import FileSerializer


class FileViewSet(AbstractAuthViewSet):
    queryset = File.objects.order_by('-id')
    serializer_class = FileSerializer
