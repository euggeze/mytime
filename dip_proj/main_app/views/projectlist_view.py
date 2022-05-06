"""Module for working with ProjectList model"""
from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet

from main_app.models import ProjectList
from main_app.rest import ProjectListSerialize


class ProjectListViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = ProjectListSerialize
    queryset = ProjectList.objects.all()

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
            pk = self.request.GET.get("pk",None)
            if pk:
                queryset = queryset.filter(employee=pk)
                return queryset
            return queryset