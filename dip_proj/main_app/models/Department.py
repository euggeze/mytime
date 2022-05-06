"""This module for create django model"""
from django.db import models


class Department(models.Model):
    """Class for object structure Department"""
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'Department'
        verbose_name = 'Department names'
        ordering = ['name']

    def __str__(self):
        return self.name
