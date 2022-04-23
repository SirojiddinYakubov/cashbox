from rest_framework import serializers

from api.v1.common.services import OrganizationService
from common.models import Organization


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'title'
        ]

    def create(self, validated_data):
        organization = OrganizationService.create_organization(validated_data)
        return organization