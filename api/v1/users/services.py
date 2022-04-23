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
        if cls._clean_user_data(employee_data):
            password = employee_data.get('password')
            employee = Employee(**employee_data, role=employee_role)
            employee.set_password(password)
            employee.save()
            return employee
        else:
            return False

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

    @classmethod
    def _clean_user_data(cls, data: dict):
        required_keys = ['organization', 'name', 'phone', 'password']
        if not all([True if x in data.keys() else False for x in required_keys]):
            raise ValueError('Все обязательные поля должны быть заполнены')

        if not data['name']:
            raise ValueError('Имя должно быть заполнено')

        if len(data['phone']) != 12:
            raise ValueError('Номер телефона должен состоять из 12 цифр')

        employee = Employee.objects.filter(phone=data['phone'])
        if employee.exists():
            raise IntegrityError("Этот номер телефона уже зарегистрирован")

        if len(data['password']) < 5:
            raise ValueError('Длина пароля должна быть больше 5')

        if not data['organization']:
            raise ObjectDoesNotExist('Организация не найдена')

        if not isinstance(data['organization'], Organization):
            raise ObjectDoesNotExist('Организация не найдена')

        return True
