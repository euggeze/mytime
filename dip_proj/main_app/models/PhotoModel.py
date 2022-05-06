"""This module for django migration"""
from django.contrib.auth.models import User
from django.db import models


class PhotoModel(models.Model):
    """Class for object structure Employee"""
    photo = models.ImageField(upload_to="case_data", null=True)

    def __str__(self):
        return self.photo