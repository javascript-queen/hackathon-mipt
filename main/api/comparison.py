from .base_viewsets import AbstractAuthViewSet
from main.models import Comparison
from main.serializers import ComparisonSerializer


class ComparisonViewSet(AbstractAuthViewSet):
    queryset = Comparison.objects.order_by('-id')
    serializer_class = ComparisonSerializer
