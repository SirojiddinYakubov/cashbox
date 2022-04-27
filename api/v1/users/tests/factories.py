import string

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy
from faker import Faker

from api.v1.common.tests.factories import OrganizationFactory

Employee = get_user_model()
faker = Faker()


class EmployeeFactory(factory.django.DjangoModelFactory):
    """ этот класс создает поддельные данные сотрудника для тестирования """

    class Meta:
        model = Employee

    name = faker.name()
    password = faker.password()
    phone = fuzzy.FuzzyText(length=9, prefix='998', chars=string.digits)
    organization = factory.SubFactory(OrganizationFactory)
    # phone = "998{0}".format(fuzzy.FuzzyInteger(100000000, 999999999).fuzz())
