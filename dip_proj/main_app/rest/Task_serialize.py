"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Task


class TaskSerialize(serializers.ModelSerializer):
    """ Class for serialization Task"""

    class Meta:
        model = Task
        fields = '__all__'