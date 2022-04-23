from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.users.services import EmployeeService

Employee = get_user_model()


class EmployeeListSerializer(serializers.ModelSerializer):
    """ serializer для список пользователей """

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'role',
            'organization',
        ]


class EmployeeCreateUserSerializer(serializers.ModelSerializer):
    """ serializer для создать пользователь user """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'organization',
            'password',
        ]
        extra_kwargs = {
            'organization': {'required': True},
            'name': {'required': True},
        }

    def create(self, validated_data):
        user = EmployeeService.create_user(validated_data)
        return user


class EmployeeCreateCashierSerializer(serializers.ModelSerializer):
    """ serializer для создать пользователь cashier (кассир) """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'organization',
            'password',
        ]
        extra_kwargs = {
            'organization': {'required': True},
            'name': {'required': True},
        }

    def create(self, validated_data):
        user = EmployeeService.create_cashier(validated_data)
        return user
