from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.v1 import permissions
from . import serializers
from .services import (
    EmployeeService
)

Employee = get_user_model()


class EmployeeListView(generics.ListAPIView):
    """ Список пользователей """
    queryset = None
    serializer_class = serializers.EmployeeListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = EmployeeService.get_employees_list()
        return qs
