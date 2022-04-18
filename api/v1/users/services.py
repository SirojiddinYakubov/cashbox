from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

Employee = get_user_model()


class EmployeeService(object):
    """ Бизнес логики для пользователей """

    @staticmethod
    def get_employees_list() -> QuerySet[Employee]:
        return Employee.objects.filter(is_active=True,
                                       role__in=[Employee.Role.USER, Employee.Role.CASHIER])
