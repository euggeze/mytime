"""Module for working with Project model"""
from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from main_app.models import Project
from main_app.rest import ProjectSerialize


class ProjectViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = ProjectSerialize
    queryset = Project.objects.all()

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
            proj = self.request.GET.get("proj",None)
            if proj:
                queryset = queryset.filter(project_name=proj)
                return queryset
            return queryset