from django.contrib.auth import get_user_model
from rest_framework import serializers

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
