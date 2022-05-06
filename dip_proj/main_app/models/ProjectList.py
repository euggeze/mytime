"""This module for create django model"""
from django.db import models


class ProjectList(models.Model):
    """Class for object structure ProjectList"""
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=False, blank=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'ProjectList'
        verbose_name = 'List of projects'
