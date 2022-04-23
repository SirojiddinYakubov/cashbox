from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = EmployeeService.get_employees_list()
        return qs


class EmployeeCreateUserView(generics.CreateAPIView):
    """ Cоздать роль user """
    queryset = None
    serializer_class = serializers.EmployeeCreateUserSerializer
    permission_classes = [
        permissions.DirectorPermission |
        permissions.AdminPermission
    ]


class EmployeeCreateCashierView(generics.CreateAPIView):
    """ Cоздать роль cashier (кассир) """
    queryset = None
    serializer_class = serializers.EmployeeCreateCashierSerializer
    permission_classes = [
        permissions.DirectorPermission |
        permissions.AdminPermission
    ]
