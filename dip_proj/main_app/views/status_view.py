"""Module for working with Status model"""
from rest_framework.viewsets import ModelViewSet

from main_app.models import Status
from main_app.rest import StatusSerialize


class StatusViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = StatusSerialize
    queryset = Status.objects.all()