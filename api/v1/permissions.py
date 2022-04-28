from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

Employee = get_user_model()


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != Employee.Role.USER:
            return False
        return request.user.is_active


class CashierPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != Employee.Role.CASHIER:
            return False
        return request.user.is_active


class DirectorPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != Employee.Role.DIRECTOR:
            return False
        return request.user.is_active


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role != Employee.Role.ADMIN:
            return False
        return request.user.is_active
