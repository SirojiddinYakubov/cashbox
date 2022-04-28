from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from api.v1 import permissions
from . import serializers
from .services import (EmployeeService, )

Employee = get_user_model()


class EmployeeListView(generics.ListAPIView):
    """ Список пользователей """
    queryset = None
    serializer_class = serializers.EmployeeListSerializer

    def get_queryset(self):
        qs = EmployeeService.get_employees_list()
        return qs


class EmployeeCreateUserView(generics.CreateAPIView):
    """ Cоздать роль user """
    queryset = None
    serializer_class = serializers.EmployeeCreateUpdateUserSerializer
    permission_classes = [
        permissions.DirectorPermission |
        permissions.AdminPermission
    ]


class EmployeeUpdateUserView(generics.UpdateAPIView):
    """ Изменение роль user """
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = serializers.EmployeeCreateUpdateUserSerializer
    permission_classes = [
        permissions.DirectorPermission |
        permissions.AdminPermission
    ]

    def get_object(self):
        obj = Employee.objects.get(pk=self.kwargs.get('pk'))
        if obj.organization == self.request.user.organization:
            return super().get_object()
        raise PermissionDenied()


class EmployeeCreateCashierView(generics.CreateAPIView):
    """ Cоздать роль cashier (кассир) """
    queryset = None
    serializer_class = serializers.EmployeeCreateUpdateCashierSerializer
    permission_classes = [
        permissions.DirectorPermission |
        permissions.AdminPermission
    ]
