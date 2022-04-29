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
    role = serializers.SerializerMethodField(method_name='get_role_display', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'phone',
            'role',
            'email',
            'organization',
            'password',
        ]
        extra_kwargs = {
            'organization': {'required': True},
        }

    def get_role_display(self, obj):
        return obj.get_role_display()

    def create(self, validated_data):
        user = EmployeeService.create_user(validated_data)
        return user

    def update(self, instance, validated_data):
        user = EmployeeService.update_user(instance, validated_data)
        return user


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
