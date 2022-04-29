import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from common.models import Organization

Employee = get_user_model()


@pytest.fixture
def create_user_data(request, api_client, employee_factory, organization_factory):
    organization = organization_factory.create()
    data = {
        'success-with-director':
            (
                status.HTTP_201_CREATED,
                api_client(employee=employee_factory.create(role=Employee.Role.DIRECTOR, organization=organization)), {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization.id,
                }
            ),
        'success-with-admin':
            (
                status.HTTP_201_CREATED,
                api_client(employee=employee_factory.create(role=Employee.Role.ADMIN, organization=organization)), {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": organization.id,
                }
            ),
        'forbidden-with-user':
            (
                status.HTTP_403_FORBIDDEN,
                api_client(employee=employee_factory.create(role=Employee.Role.USER, organization=organization)), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'forbidden-with-cashier':
            (
                status.HTTP_403_FORBIDDEN,
                api_client(employee=employee_factory.create(role=Employee.Role.CASHIER, organization=organization)), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'error-with-unregistered-user':
            (
                status.HTTP_401_UNAUTHORIZED, api_client(), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize("create_user_data", ['success-with-director', 'success-with-admin', 'forbidden-with-user',
                                              'forbidden-with-cashier', 'error-with-unregistered-user'], indirect=True)
def test_create_user(create_user_data):
    url = reverse_lazy('users:employee_create_user')
    status_code, client, data = create_user_data
    response = client.post(url, data=data)
    assert response.status_code == status_code
    if response.status_code == status.HTTP_201_CREATED:
        assert response.json()


@pytest.fixture
def update_user_data(request, employee_factory, organization_factory, api_client):
    organization = organization_factory.create()
    data = {
        'success-with-director':
            (
                status.HTTP_200_OK,
                api_client(employee=employee_factory.create(role=Employee.Role.DIRECTOR, organization=organization)), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'success-with-admin':
            (
                status.HTTP_200_OK,
                api_client(employee=employee_factory.create(role=Employee.Role.ADMIN, organization=organization)), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'forbidden-with-user':
            (
                status.HTTP_403_FORBIDDEN,
                api_client(employee=employee_factory.create(role=Employee.Role.USER, organization=organization)),
                {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'forbidden-with-cashier':
            (
                status.HTTP_403_FORBIDDEN,
                api_client(employee=employee_factory.create(role=Employee.Role.CASHIER, organization=organization)),
                {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
        'error-with-unregistered-user':
            (
                status.HTTP_401_UNAUTHORIZED, api_client(), {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": organization.id,
                }
            ),
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize("update_user_data", ['success-with-director',
                                              'success-with-admin', 'forbidden-with-user',
                                              'forbidden-with-cashier', 'error-with-unregistered-user'
                                              ], indirect=True)
def test_update_user(update_user_data, employee_factory):
    status_code, client, data = update_user_data
    organization = Organization.objects.get(id=data['organization'])
    # create instance
    instance = employee_factory.create(role=Employee.Role.USER, organization=organization)
    # send post request
    url = reverse_lazy('users:employee_update_user', kwargs={'pk': instance.id})
    response = client.patch(url, data=data)
    # check response
    assert response.status_code == status_code
    if response.status_code == status.HTTP_200_OK:
        assert response.json()


@pytest.fixture
def employee_list_test_fixture(request, api_client, employee_factory):
    data = {
        'success-with-registered-user':
            (status.HTTP_200_OK, api_client(employee=employee_factory.create(role=Employee.Role.USER))),
        'error-with-unregistered-user':
            (status.HTTP_401_UNAUTHORIZED, api_client()),
    }
    return data[request.param]


@pytest.mark.parametrize("employee_list_test_fixture",
                         ['success-with-registered-user', 'error-with-unregistered-user'], indirect=True)
@pytest.mark.django_db
def test_employee_list(employee_list_test_fixture, employee_factory):
    status_code, client = employee_list_test_fixture
    batch_size = 4
    employee_factory.create_batch(batch_size)
    url = reverse_lazy('users:employee_list')
    response = client.get(url)
    assert response.status_code == status_code
    if response.status_code == status.HTTP_200_OK:
        assert response.json().get('results')
