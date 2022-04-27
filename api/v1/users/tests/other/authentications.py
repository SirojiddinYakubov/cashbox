from functools import wraps

from django.contrib.auth import get_user_model
from factory import fuzzy
from faker import Faker
from rest_framework import status

from conf import settings

Employee = get_user_model()


def _get_authentication_token(self, phone, password):
    url = '/api/v1/auth/jwt/create/'
    response = self.client.post(url, data={'phone': phone, 'password': password})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.json())
    return response.json()['access']


def _authenticate(func, role):
    @wraps(func)
    def wrapper(*args, **kwargs):
        faker = Faker()
        password = faker.password()
        phone = "998{0}".format(fuzzy.FuzzyInteger(100000000, 999999999).fuzz())
        data = {
            'phone': phone,
            'name': "Test user for authenticate",
            'role': role,
        }
        employeee = Employee(**data)
        employeee.set_password(password)
        employeee.save()

        self = args[0]
        token = _get_authentication_token(self, phone, password)
        self.client.credentials(HTTP_AUTHORIZATION=settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0] + ' ' + token)
        return func(*args, **kwargs)

    return wrapper


def director_authenticate(func):
    return _authenticate(func, Employee.Role.DIRECTOR)


def cashier_authenticate(func):
    return _authenticate(func, Employee.Role.CASHIER)


def user_authenticate(func):
    return _authenticate(func, Employee.Role.USER)