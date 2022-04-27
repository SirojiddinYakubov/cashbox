import factory
from common.models import Organization
from faker import Faker

faker = Faker()


class OrganizationFactory(factory.django.DjangoModelFactory):
    """ этот класс создает поддельные данные организация для тестирования """

    class Meta:
        model = Organization

    title = faker.company()
