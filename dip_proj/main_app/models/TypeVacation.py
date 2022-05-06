"""This module for create django model"""
from django.db import models


class TypeVacation(models.Model):
    """Class for object structure TypeVacation"""
    type_vacation = models.CharField(max_length=30, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'TypeVacation'
        verbose_name = 'Types vacation'

    def __str__(self):
        return self.type_vacation
