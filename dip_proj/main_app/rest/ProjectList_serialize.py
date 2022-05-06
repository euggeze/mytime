"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import ProjectList


class ProjectListSerialize(serializers.ModelSerializer):
    """ Class for serialization ProjectList"""

    class Meta:
        model = ProjectList
        fields = '__all__'