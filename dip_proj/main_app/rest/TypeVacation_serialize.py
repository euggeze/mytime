"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import TypeVacation


class TypeVacationSerialize(serializers.ModelSerializer):
    """ Class for serialization Employees"""

    class Meta:
        model = TypeVacation
        fields = '__all__'