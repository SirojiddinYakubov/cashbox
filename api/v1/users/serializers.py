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


class EmployeeCreateUpdateUserSerializer(serializers.ModelSerializer):
    """ serializer для создать пользователь user """
    password = serializers.CharField(write_only=True, min_length=5, required=True)
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

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
        }

    def create(self, validated_data):
        user = EmployeeService.create_user(validated_data)
        return user

    def update(self, instance, validated_data):
        print(instance, validated_data)
        return instance

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['role'] = instance.get_role_display()
        return context


class EmployeeCreateUpdateCashierSerializer(serializers.ModelSerializer):
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
            'password': {'required': False}
        }

    def create(self, validated_data):
        user = EmployeeService.create_cashier(validated_data)
        return user
