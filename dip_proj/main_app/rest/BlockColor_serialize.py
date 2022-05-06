"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import BlockColor


class BlockColorSerialize(serializers.ModelSerializer):
    """ Class for serialization Level"""

    class Meta:
        model = BlockColor
        fields = '__all__'