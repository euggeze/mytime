"""Module for working with Task model"""
from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from main_app.models import Task
from main_app.rest import TaskSerialize


class TaskViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = TaskSerialize
    queryset = Task.objects.all()

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
            task = self.request.GET.get("task",None)
            if task:
                queryset = queryset.filter(task_name=task)
                return queryset
            return queryset