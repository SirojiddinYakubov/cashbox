import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from rest_framework.test import APIClient

from api.v1.common.tests.factories import OrganizationFactory
from api.v1.users.tests.factories import EmployeeFactory

register(EmployeeFactory)
register(OrganizationFactory)

Employee = get_user_model()


@pytest.fixture
def test_employee_user(db, employee_factory):
    return employee_factory.create(role=Employee.Role.USER)


@pytest.fixture
def test_employee_cashier(db, employee_factory):
    return employee_factory.create(role=Employee.Role.CASHIER)


@pytest.fixture
def test_employee_director(db, employee_factory):
    return employee_factory.create(role=Employee.Role.DIRECTOR)


@pytest.fixture
def test_employee_admin(db, employee_factory):
    return employee_factory.create(role=Employee.Role.ADMIN)


@pytest.fixture(scope='function')
def test_organization(db, organization_factory):
    return organization_factory.create()


@pytest.fixture(scope='function')
def test_organization2(db, organization_factory):
    return organization_factory.create()


@pytest.fixture
def api_client_user(test_employee_user):
    client = APIClient()
    client.force_authenticate(test_employee_user)
    return client


@pytest.fixture
def api_client_cashier(test_employee_cashier):
    client = APIClient()
    client.force_authenticate(test_employee_cashier)
    return client


@pytest.fixture
def api_client_director(test_employee_director):
    client = APIClient()
    client.force_authenticate(test_employee_director)
    return client


@pytest.fixture
def api_client_admin(test_employee_admin):
    client = APIClient()
    client.force_authenticate(test_employee_admin)
    return client
