"""This module for create django model"""
from django.db import models


class StatusVacation(models.Model):
    """Class for object structure Status"""
    status_vacation = models.CharField(max_length=30, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'StatusVacation'
        verbose_name = 'Status vac names'

    def __str__(self):
        return self.status_vacation
