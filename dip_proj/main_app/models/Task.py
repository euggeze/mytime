"""This module for create django model"""
from django.db import models


class Task(models.Model):
    """Class for object structure Task"""
    task_name = models.CharField(max_length=120, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'Task'
        verbose_name = 'Task names'
