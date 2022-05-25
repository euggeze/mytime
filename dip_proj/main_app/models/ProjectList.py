"""This module for create django model"""
from django.db import models


class ProjectList(models.Model):
    """Class for object structure ProjectList"""
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=False, blank=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, blank=False)
    workload = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        db_table = 'ProjectList'
        verbose_name = 'List of projects'
