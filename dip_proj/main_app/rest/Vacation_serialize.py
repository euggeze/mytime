"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Vacation


class VacationSerialize(serializers.ModelSerializer):
    """ Class for serialization Vacation"""

    class Meta:
        model = Vacation
        fields = '__all__'