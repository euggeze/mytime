"""Module for working with Level model"""
from rest_framework.viewsets import ModelViewSet

from main_app.models import Level
from main_app.rest import LevelSerialize


class LevelViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = LevelSerialize
    queryset = Level.objects.all()