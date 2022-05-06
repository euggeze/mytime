"""This module for django migration"""
from django.db import models


class Vacation(models.Model):
    """Class for object structure Vacation"""
    start_date = models.DateField(null=False, blank=False)
    finish_date = models.DateField(null=False, blank=False)
    photo_approve = models.ImageField(null=True, upload_to="vacation")
    comment_emp = models.CharField(max_length=500, null=True, blank=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=False, blank=False)
    type_vacation = models.ForeignKey('TypeVacation', on_delete=models.SET_NULL, null=True, blank=False)
    status_vacation = models.ForeignKey('StatusVacation', on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        db_table = 'Vacation'
        verbose_name = 'Vacation information'
        ordering = ['-start_date']
