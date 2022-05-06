"""This module for django migration"""
from django.db import models


class Timesheet(models.Model):
    """Class for object structure Timesheet"""
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=False, blank=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, blank=False)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=False)
    task_time = models.IntegerField(null=True, blank=False)
    task_date = models.DateField(null=True, blank=False)

    class Meta:
        db_table = 'Timesheet'
        verbose_name = 'Timesheet information'
