import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy


@pytest.fixture
def create_user_data(request, test_organization, api_client_user, api_client_cashier, api_client_director,
                     api_client_admin):
    data = {
        'success-with-director':
            (
                status.HTTP_201_CREATED, api_client_director, {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization.id,
                }
            ),
        'success-with-admin':
            (
                status.HTTP_201_CREATED, api_client_admin, {
                    "name": "John", "password": "admin12345", "phone": "998919791999",
                    "organization": test_organization.id,
                }
            ),
        'forbidden-with-user':
            (
                status.HTTP_403_FORBIDDEN, api_client_user, {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": test_organization.id,
                }
            ),
        'forbidden-with-cashier':
            (
                status.HTTP_403_FORBIDDEN, api_client_cashier, {
                    "name": "Nick", "password": "qwerty12345", "phone": "998906366264",
                    "organization": test_organization.id,
                }
            ),
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize("create_user_data", ['success-with-director', 'success-with-admin', 'forbidden-with-user',
                                              'forbidden-with-cashier'], indirect=True)
def test_create_user(create_user_data):
    url = reverse_lazy('users:employee_create_user')
    status_code, client, data = create_user_data
    response = client.post(url, data=data)
    assert response.status_code == status_code
    if response.status_code == status.HTTP_201_CREATED:
        assert sorted(['id', 'name', 'phone', 'email', 'role', 'organization']) == sorted(response.json().keys())
