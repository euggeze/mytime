"""This module for create django model"""
from django.db import models


class BlockColor(models.Model):
    """Class for object structure Task"""
    background_color = models.CharField(max_length=10, null=False, blank=False, unique=True)
    progress_color = models.CharField(max_length=10, null=False, blank=False, unique=True)


