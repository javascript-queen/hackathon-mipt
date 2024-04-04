from .base_viewsets import AbstractAuthViewSet
from main.models import Doc
from main.serializers import DocSerializer


class DocViewSet(AbstractAuthViewSet):
    queryset = Doc.objects.order_by('-id')
    serializer_class = DocSerializer
