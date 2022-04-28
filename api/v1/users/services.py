from typing import Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.query import QuerySet

from common.models import Organization

Employee = get_user_model()


class EmployeeService(object):
    """ Бизнес логики для пользователей """

    @classmethod
    def _base_create_employee(cls, employee_data, employee_role):
        password = employee_data.get('password')
        if employee_data.get('role', None):
            employee_data.pop('role')
        employee = Employee(**employee_data, role=employee_role)
        employee.set_password(password)
        employee.save()
        return employee

    @classmethod
    def create_user(cls, data: dict) -> Union[Employee, bool]:
        return cls._base_create_employee(data, Employee.Role.USER)

    @classmethod
    def create_cashier(cls, data: dict) -> Union[Employee, bool]:
        return cls._base_create_employee(data, Employee.Role.CASHIER)

    @classmethod
    def get_employees_list(cls) -> QuerySet[Employee]:
        return Employee.objects.filter(is_active=True,
                                       role__in=[Employee.Role.USER, Employee.Role.CASHIER]
                                       )
