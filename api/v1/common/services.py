from typing import Union

from django.db.models import QuerySet

from common.models import Organization


class OrganizationService(object):
    """ Бизнес логики для организацией """

    @classmethod
    def create_organization(cls, data) -> Union[Organization, bool]:
        if cls._clean_organization_data(data):
            organization = Organization(**data)
            organization.save()
            return organization
        else:
            return False

    @classmethod
    def _clean_organization_data(cls, data: dict) -> bool:
        if 'title' in data and data['title']:
            return True
        return False