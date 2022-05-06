"""This module for create django model"""
from django.db import models


class Level(models.Model):
    """Class for object structure Level"""
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'Level'
        verbose_name = 'Level names'
        ordering = ['name']
