from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from api.v1.users.services import EmployeeService
from common.models import Organization

Employee = get_user_model()


class EmployeeTestCase(APITestCase):
    """ Убедитесь, что вы получили список пользователей """
    def setUp(self) -> None:
        self.organization = Organization.objects.create(title="Test organization")
        self.user = Employee.objects.create_user(phone='998919791999', organization=self.organization,
                                                 name="Sirojiddin Yakubov", password='testpassword')
        self.service = EmployeeService()

    def test_employee_list_service(self) -> None:
        employees_list = self.service.get_employees_list()
        self.assertEqual(employees_list.count(), 1)
        self.assertEqual(employees_list[0].phone, '998919791999')
        self.assertEqual(employees_list[0].role, Employee.Role.USER)
        self.assertEqual(employees_list[0].organization, self.organization)
