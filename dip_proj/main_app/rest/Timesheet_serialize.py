"""Module for serialization information"""
from rest_framework import serializers

from main_app.models import Timesheet


class TimesheetSerialize(serializers.ModelSerializer):
    """ Class for serialization Timesheet"""

    class Meta:
        model = Timesheet
        fields = '__all__'