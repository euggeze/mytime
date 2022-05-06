"""Module for working with Vacation model"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission


from main_app.rest import UserSerialize


class UserViewSet(ModelViewSet):
    """Class for selecting queryset and
        serializer_class"""
    serializer_class = UserSerialize
    queryset = User.objects.all()
    
