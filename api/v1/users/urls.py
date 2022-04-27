from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('employee/list/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/create/user/', views.EmployeeCreateUserView.as_view(), name='employee_create_user'),
    path('employee/update/user/<int:pk>/', views.EmployeeUpdateUserView.as_view(), name='employee_update_user'),
    path('employee/create/cashier/', views.EmployeeCreateCashierView.as_view(), name='employee_create_cashier'),
]
