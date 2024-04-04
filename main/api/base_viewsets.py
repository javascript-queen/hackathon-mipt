from rest_framework import viewsets
from rest_framework import permissions


class AbstractAuthViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
