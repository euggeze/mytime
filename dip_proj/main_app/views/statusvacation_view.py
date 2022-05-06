"""Module for working with StatusVacation model"""
from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet

from main_app.models import StatusVacation
from main_app.rest import StatusVacationSerialize


class StatusVacationViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = StatusVacationSerialize
    queryset = StatusVacation.objects.all()

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
            status_vac = self.request.GET.get("status_vac",None)
            if status_vac:
                queryset = queryset.filter(status_vacation=status_vac)
                return queryset
            return queryset