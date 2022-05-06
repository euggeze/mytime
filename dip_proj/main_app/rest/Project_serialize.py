"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Project


class ProjectSerialize(serializers.ModelSerializer):
    """ Class for serialization Project"""

    class Meta:
        model = Project
        fields = '__all__'