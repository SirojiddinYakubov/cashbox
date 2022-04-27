import pytest

from pytest_factoryboy import register
from api.v1.common.tests.factories import OrganizationFactory

register(OrganizationFactory)


@pytest.fixture
def new_organization1(db, organization_factory):
    organization = organization_factory.create()
    return organization
