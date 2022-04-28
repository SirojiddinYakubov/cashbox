import pytest
from django.contrib.auth import get_user_model

from api.v1.users import services

Employee = get_user_model()


@pytest.fixture
def create_user_data(request, test_organization, test_organization2):
    data = {
        'valid-data':
            (
                True,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization, 'role': Employee.Role.USER
                },

            ),
        'invalid-name':
            (
                False,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John2", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization, 'role': Employee.Role.USER
                },
            ),
        'invalid-password':
            (
                False,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John", "password": "admin123", "phone": "998919791999",
                    "organization": test_organization, 'role': Employee.Role.USER
                },
            ),
        'invalid-phone':
            (
                False,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791998",
                    "organization": test_organization, 'role': Employee.Role.USER
                },
            ),
        'invalid-organization':
            (
                False,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization2, 'role': Employee.Role.USER
                },
            ),
        'invalid-role':
            (
                False,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization, 'role': Employee.Role.CASHIER
                },
            ),
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize("create_user_data",
                         ['valid-data', 'invalid-name', 'invalid-password', 'invalid-phone', 'invalid-organization',
                          'invalid-role'], indirect=True)
def test_create_user(create_user_data):
    validity, data, confirm_data = create_user_data
    user = services.EmployeeService.create_user(data=data)
    assert all([user.name == confirm_data.get('name'),
                user.phone == confirm_data.get('phone'),
                user.organization == confirm_data.get('organization'),
                user.role == confirm_data.get('role'),
                user.check_password(confirm_data.get('password'))]) == validity
    assert 1 == Employee.objects.count()
