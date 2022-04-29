import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from api.v1.common.tests.factories import OrganizationFactory
from api.v1.users.tests.factories import EmployeeFactory

register(EmployeeFactory)
register(OrganizationFactory)


@pytest.fixture
def api_client():
    def _api_client(employee=None):
        client = APIClient()
        if employee:
            client.force_authenticate(employee)
        return client

    return _api_client
