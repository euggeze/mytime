"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Status


class StatusSerialize(serializers.ModelSerializer):
    """ Class for serialization Status"""

    class Meta:
        model = Status
        fields = '__all__'