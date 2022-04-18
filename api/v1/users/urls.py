from django.urls import path
from . import views

urlpatterns = [
    path('employee/list/', views.EmployeeListView.as_view(), name='employee_list'),
]
