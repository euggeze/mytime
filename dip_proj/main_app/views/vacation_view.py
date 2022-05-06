"""Module for working with Vacation model"""
from django.db.models import QuerySet
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from main_app.models import Vacation
from main_app.rest import VacationSerialize


class VacationViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = VacationSerialize
    queryset = Vacation.objects.all()


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
            employee = self.request.GET.get("employee",None)
            vac_type = self.request.GET.get("vac_type",None)
            if employee and not vac_type:
                queryset = queryset.filter(employee=employee)
                return queryset
            status = "Approval"
            if employee and vac_type:
                queryset = queryset.filter(employee=employee,status_vacation=status,type_vacation=vac_type)
                return queryset
            return queryset