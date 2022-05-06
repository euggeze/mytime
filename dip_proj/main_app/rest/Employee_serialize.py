"""Module for serialization information"""
import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from main_app.models import Employee, Vacation


class EmployeeSerialize(serializers.ModelSerializer):
    """ Class for serialization Employee"""
    count_paid_vac = SerializerMethodField('get_paid_vac')

    @staticmethod
    def get_paid_vac(obj):
        """Method for counting the average salary of a department
            Keyword argument:
            obj - current object Employee
            Return:
            Count days paid vacation in year
        """
        employee_data = Vacation.objects.filter(employee=obj)
        res = 0
        for x in employee_data:
            if x.type_vacation == 'Paid leave' and x.status_vacation == "Approved":
                if x.start_date>datetime.datetime.now().date().replace(month=1, day=1) and x.finish_date <datetime.datetime.now().date().replace(month=12, day=31):
                    res+= (x.finish_date-x.start_date).days
                elif x.start_date<datetime.datetime.now().date().replace(month=1, day=1) and x.finish_date<datetime.datetime.now().date().replace(month=12, day=31):
                    res += (x.finish_date - datetime.datetime.now().date().replace(month=1, day=1)).days
                elif x.start_date >datetime.datetime.now().date().replace(month=1, day=1) and x.finish_date>datetime.datetime.now().date().replace(month=12, day=31):
                    res += (datetime.datetime.now().date().replace(month=12, day=31)-x.start_date).days
        return 28-res
    class Meta:
        model = Employee
        fields = '__all__'