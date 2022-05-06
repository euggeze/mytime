"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import PhotoModel


class PhotoModelSerialize(serializers.ModelSerializer):
    """ Class for serialization Project"""

    class Meta:
        model = PhotoModel
        fields = '__all__'