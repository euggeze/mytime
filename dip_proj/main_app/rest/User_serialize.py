"""Module for serialization information"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerialize(serializers.ModelSerializer):
    """ Class for serialization Department"""

    class Meta:
        model = User
        fields = '__all__'
