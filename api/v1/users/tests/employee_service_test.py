import pytest
from django.contrib.auth import get_user_model

from api.v1.users.serializers import EmployeeCreateUserSerializer
from common.models import Organization

Employee = get_user_model()


@pytest.mark.parametrize(
    "data, validity",
    [
        pytest.param({
            "name": "John",
            "password": "admin12345",
            "phone": "998919791999",
            "organization": 1
        },
            True,
            id="complete-data",
        ),
        pytest.param({
            "password": "admin12345",
            "phone": "998919791999",
            "organization": 1
        },
            False,
            id="missing-name",
        ),
        pytest.param({
            "name": "John",
            "password": "admin12345",
            "phone": "998919791999",
        },
            False,
            id="missing-organization",
        ),
    ],
)
def test_employee_create(test_organization, data, validity):
    # org_id = dict(data).get('organization', None)
    # if org_id:
    #     org = Organization.objects.get(id=org_id)
    #     print(org)
    serializer = EmployeeCreateUserSerializer(data=data)
    assert serializer.is_valid() == validity
