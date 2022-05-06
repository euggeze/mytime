"""This module for django migration"""
from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    """Class for object structure Employee"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=False, blank=False)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True, blank=False)
    position = models.CharField(max_length=40, null=True, blank=False)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=False)
    photo = models.ImageField(upload_to="case_data", null=True)
    manager = models.IntegerField(null=True)

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee information'
        ordering = ['level', 'last_name']

    def __str__(self):
        return self.first_name + " " +self.last_name