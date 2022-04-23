from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.v1.users.services import EmployeeService
from api.v1.users.tests.authentications import director_authenticate, user_authenticate
from api.v1.users.tests.factory import UserFactory, OrganizationFactory

Employee = get_user_model()


class CreateServiceTestCase(APITestCase):
    """ Тестирование создать пользователь user, cashier service """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.organization_object = OrganizationFactory.create()
        cls.create_jwt_url = '/api/v1/auth/jwt/create/'

        cls.valid_data = {
            'name': cls.user_object.name,
            'phone': cls.user_object.phone,
            'password': cls.user_object.password,
            'organization': cls.organization_object
        }
        cls.invalid_data = {
            'name': cls.user_object.name,
            'phone': cls.user_object.phone,
            'password': cls.user_object.password,
            # 'organization': cls.organization_object
        }

    def test_create_user_service_with_valid_data(self):
        EmployeeService.create_user(data=self.valid_data)
        self.assertEqual(Employee.objects.count(), 1)
        user = Employee.objects.first()
        self.assertEqual(user.role, Employee.Role.USER)
        self.assertEqual(user.name, self.user_object.name)
        self.assertEqual(user.phone, self.user_object.phone)
        self.assertEqual(user.organization, self.organization_object)
        self._check_employee_password_correct_saved_to_db(phone=self.user_object.phone, password=self.user_object.password)

    def test_create_user_service_with_invalid_data(self):
        with self.assertRaises(Exception):
            EmployeeService.create_user(data=self.invalid_data)
        self.assertEqual(Employee.objects.count(), 0)

    def test_create_cashier_service_with_valid_data(self):
        EmployeeService.create_cashier(data=self.valid_data)
        self.assertEqual(Employee.objects.count(), 1)
        user = Employee.objects.first()
        self.assertEqual(user.role, Employee.Role.CASHIER)
        self.assertEqual(user.name, self.user_object.name)
        self.assertEqual(user.phone, self.user_object.phone)
        self.assertEqual(user.organization, self.organization_object)
        self._check_employee_password_correct_saved_to_db(phone=self.user_object.phone, password=self.user_object.password)

    def test_create_cashier_service_with_invalid_data(self):
        with self.assertRaises(Exception):
            EmployeeService.create_cashier(data=self.invalid_data)
        self.assertEqual(Employee.objects.count(), 0)

    def test_if_employee_phone_already_exists(self):
        EmployeeService.create_user(data=self.valid_data)
        self.assertEqual(Employee.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            EmployeeService.create_user(data=self.valid_data)
            EmployeeService.create_cashier(data=self.valid_data)
        self.assertEqual(Employee.objects.count(), 1)

    def _check_employee_password_correct_saved_to_db(self, phone: str, password: str):
        data = {
            'phone': phone,
            'password': password
        }
        response = self.client.post(self.create_jwt_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())


class UserCreateViewTestCase(APITestCase):
    """ Тестирование создать пользователь user view """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.organization_object = OrganizationFactory.create()
        cls.client = APIClient()
        cls.url = reverse('users:employee_create_user')

        cls.valid_data = {
            'name': cls.user_object.name,
            'phone': cls.user_object.phone,
            'password': cls.user_object.password,
            'organization': cls.organization_object.id
        }
        cls.invalid_data = {
            'name': cls.user_object.name,
            'phone': cls.user_object.phone,
            'password': cls.user_object.password,
            # 'organization': cls.organization_object.id
        }

    @director_authenticate
    def test_create_user_view_with_valid_data(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(list(response.data.keys()), ['id', 'name', 'phone', 'email', 'organization'])

        self.assertEqual(Employee.objects.count(), 2)

        new_user = Employee.objects.get(phone=self.user_object.phone)

        self.assertEqual(
            new_user.organization,
            self.organization_object,
        )
        self.assertEqual(
            new_user.phone,
            self.user_object.phone,
        )

    @director_authenticate
    def test_create_user_view_with_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Employee.objects.count(), 1)

    @user_authenticate
    def test_create_user_view_with_other_role(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Employee.objects.count(), 1)


class EmployeeListServiceTestCase(APITestCase):
    """ Тестирование списки пользователя сервис """

    @director_authenticate
    def test_check_employee_list_filter_allowed_role(self):
        qs = EmployeeService.get_employees_list()
        roles = set(qs.values_list('role', flat=True))
        self.assertNotIn(Employee.Role.ADMIN, roles)
        self.assertNotIn(Employee.Role.DIRECTOR, roles)
