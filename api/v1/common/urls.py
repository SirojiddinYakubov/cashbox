from django.urls import path
from . import views

urlpatterns = [
    path('organization/create/', views.OrganizationCreateView.as_view(), name='organization_create')
]
