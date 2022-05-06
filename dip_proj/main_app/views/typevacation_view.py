"""Module for working with TypeVacation model"""
from rest_framework.viewsets import ModelViewSet

from main_app.models import TypeVacation
from main_app.rest import TypeVacationSerialize


class TypeVacationViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = TypeVacationSerialize
    queryset = TypeVacation.objects.all()