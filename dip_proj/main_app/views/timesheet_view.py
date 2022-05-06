"""Module for working with Timesheet model"""
from datetime import datetime, timedelta

from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet

from main_app.models import Timesheet
from main_app.rest import TimesheetSerialize


class TimesheetViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = TimesheetSerialize
    queryset = Timesheet.objects.all()

    def get_queryset(self):
        """Custom function for working with a filter"""
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
            pk = self.request.GET.get("pk")
            start = self.request.GET.get("start", None)
            end = self.request.GET.get("finish", None)
            task = self.request.GET.get("task", None)
            if task:
                queryset = queryset.filter(task=task)
                return queryset
            if start and end:
                queryset = queryset.filter(employee=pk)
                queryset = queryset.filter(task_date__range=[start, end])
                return queryset
            elif start and not end:
                queryset = queryset.filter(employee=pk)
                queryset = queryset.filter(task_date__range=[start, datetime.today()])
                return queryset
            elif pk:
                queryset = queryset.filter(employee=pk)
                weekday = datetime.today().weekday()
                queryset = queryset.filter(task_date__range=[datetime.today()-timedelta(weekday), datetime.today()+timedelta(5-weekday)])
                return queryset
            return queryset

