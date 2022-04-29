import pytest
from django.contrib.auth import get_user_model

from api.v1.users import services

Employee = get_user_model()


@pytest.fixture
def create_update_user_data(request, employee_factory, organization_factory):
    organization1, organization2 = organization_factory.create_batch(2)
    user = employee_factory.create()
    data = {
        'valid-data':
            (
                True, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1, 'role': Employee.Role.USER
                },

            ),
        'invalid-name':
            (
                False, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John2", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1, 'role': Employee.Role.USER
                },
            ),
        'invalid-password':
            (
                False, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John", "password": "admin123", "phone": "998919791999",
                    "organization": organization1, 'role': Employee.Role.USER
                },
            ),
        'invalid-phone':
            (
                False, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791998",
                    "organization": organization1, 'role': Employee.Role.USER
                },
            ),
        'invalid-organization':
            (
                False, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization2, 'role': Employee.Role.USER
                },
            ),
        'invalid-role':
            (
                False, user,
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1
                },
                {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization1, 'role': Employee.Role.CASHIER
                },
            ),
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize("create_update_user_data",
                         ['valid-data', 'invalid-name', 'invalid-password', 'invalid-phone', 'invalid-organization',
                          'invalid-role'], indirect=True)
def test_create_user(create_update_user_data):
    validity, _, data, confirm_data = create_update_user_data
    user = services.EmployeeService.create_user(data=data)
    assert all([user.phone == confirm_data.get('phone'),
                user.name == confirm_data.get('name'),
                user.organization == confirm_data.get('organization'),
                user.role == confirm_data.get('role'),
                user.check_password(confirm_data.get('password'))]) == validity
    # if data valid check db
    if validity:
        assert Employee.objects.get(phone=confirm_data.get('phone'))
        assert 2 == Employee.objects.count()


@pytest.mark.django_db
@pytest.mark.parametrize("create_update_user_data",
                         ['valid-data', 'invalid-name', 'invalid-password', 'invalid-phone', 'invalid-organization',
                          'invalid-role'], indirect=True)
def test_update_user(create_update_user_data):
    validity, instance, data, confirm_data = create_update_user_data
    user = services.EmployeeService.update_user(instance=instance, data=data)
    assert all([user.name == confirm_data.get('name'),
                user.phone == confirm_data.get('phone'),
                user.organization == confirm_data.get('organization'),
                user.role == confirm_data.get('role'),
                user.check_password(confirm_data.get('password'))]) == validity
    # if data valid check db
    if validity:
        assert Employee.objects.filter(phone=data['phone'])
        assert 1 == Employee.objects.count()
