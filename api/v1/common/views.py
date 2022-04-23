from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.v1 import permissions
from common.models import (Organization)
from . import serializers

class OrganizationCreateView(generics.CreateAPIView):
    """ Создать организацию """
    queryset = Organization.objects.filter(is_active=True)
    serializer_class = serializers.OrganizationCreateSerializer
    permission_classes = [permissions.AdminPermission]