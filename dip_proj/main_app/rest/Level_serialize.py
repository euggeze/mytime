"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Level


class LevelSerialize(serializers.ModelSerializer):
    """ Class for serialization Level"""

    class Meta:
        model = Level
        fields = '__all__'