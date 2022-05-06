"""This module for create django model"""
from django.db import models


class Status(models.Model):
    """Class for object structure Status"""
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'Status'
        verbose_name = 'Status names'

    def __str__(self):
        return self.name
