from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class EmployeeManager(BaseUserManager):
    """ Менеджер создания пользователей """
    def create_user(self, phone, password, **extra_fields):

        if not phone:
            raise ValueError(_('Тел номер должна быть установлена'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)