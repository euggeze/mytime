"""This module for create django model"""
from django.db import models


class Project(models.Model):
    """Class for object structure Project"""
    project_name = models.CharField(max_length=40, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'Project'
        verbose_name = 'Project names'
