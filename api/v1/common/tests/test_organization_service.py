from rest_framework.test import APITestCase

from api.v1.common.services import OrganizationService
from common.models import Organization


class OrganizationCreateTestCase(APITestCase):
    """ Тестирование создать организацию """

    def setUp(self) -> None:
        self.valid_data = {
            'title': "Opensoft",
        }
        self.invalid_data = {
            'title': None,
        }

    def test_create_organization_with_valid_data(self) -> None:
        OrganizationService.create_organization(data=self.valid_data)
        self.assertEqual(Organization.objects.count(), 1)
        organization = Organization.objects.first()
        self.assertEqual(organization.title, self.valid_data['title'])


    def test_create_organization_with_invalid_data(self) -> None:
        OrganizationService.create_organization(data=self.invalid_data)
        self.assertEqual(Organization.objects.count(), 0)
