"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import StatusVacation


class StatusVacationSerialize(serializers.ModelSerializer):
    """ Class for serialization StatusVacation"""

    class Meta:
        model = StatusVacation
        fields = '__all__'