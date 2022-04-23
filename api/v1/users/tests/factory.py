from django.contrib.auth import get_user_model
from factory import django, Faker, fuzzy

from common.models import Organization

Employee = get_user_model()


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = Employee

    name = Faker('name')
    phone = "998{0}".format(fuzzy.FuzzyInteger(100000000, 999999999).fuzz())
    password = Faker('password')


class OrganizationFactory(django.DjangoModelFactory):
    class Meta:
        model = Organization

    title = Faker('company')
