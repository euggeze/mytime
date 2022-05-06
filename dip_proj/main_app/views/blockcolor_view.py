"""Module for working with Level model"""
from rest_framework.viewsets import ModelViewSet

from main_app.models import BlockColor
from main_app.rest import BlockColorSerialize


class BlockColorViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = BlockColorSerialize
    queryset = BlockColor.objects.all()