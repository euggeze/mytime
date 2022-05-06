"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Department


class DepartmentSerialize(serializers.ModelSerializer):
    """ Class for serialization Department"""

    class Meta:
        model = Department
        fields = '__all__'