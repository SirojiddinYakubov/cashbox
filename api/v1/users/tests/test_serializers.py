import pytest
from django.contrib.auth import get_user_model

from api.v1.users import serializers

Employee = get_user_model()


@pytest.fixture
def user_create_update_data(request, test_organization):
    data = {
        'complete-data':
            (
                True, {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization.id
                }
            ),
        'missing-name':
            (
                False, {
                    "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization.id
                }
            ),
        'empty-name':
            (
                False, {
                    "name": "", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization.id
                }
            ),
        'missing-password':
            (
                False, {
                    "name": "John", "phone": "998919791999", "organization": test_organization.id
                }
            ),
        'empty-password':
            (
                False, {
                    "name": "John", "password": "", "phone": "998919791999", "organization": test_organization.id
                }
            ),
        'missing-phone':
            (
                False, {
                    "name": "John", "password": "admin12345", "organization": test_organization.id
                }
            ),
        'empty-phone':
            (
                False, {
                    "name": "John", "password": "admin12345", "phone": "", "organization": test_organization.id
                }
            ),
        'missing-organization':
            (
                False, {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                }
            ),
        'invalid-organization':
            (
                False, {
                    "name": "John", "password": "admin12345", "phone": "998919791999", "organization": 1234
                }
            ),
    }
    return data[request.param]


@pytest.mark.parametrize("user_create_update_data",
                         ['complete-data', 'missing-name', 'empty-name', 'missing-password', 'empty-password',
                          'missing-phone', 'empty-phone', 'missing-organization', 'invalid-organization'],
                         indirect=True)
def test_employee_user_create_update_serializer(user_create_update_data: tuple):
    validity, data = user_create_update_data
    serializer = serializers.EmployeeCreateUpdateUserSerializer(data=data)
    assert serializer.is_valid() == validity


@pytest.mark.django_db
def test_employee_list_serializer(employee_factory):
    batch_size = 4
    employee_factory.create_batch(batch_size)
    employees = Employee.objects.all()
    serializer = serializers.EmployeeListSerializer(employees, many=True)
    assert batch_size == len(serializer.data)
    assert sorted(['id', 'name', 'phone', 'email', 'role', 'organization']) == sorted(dict(serializer.data[0]).keys())
