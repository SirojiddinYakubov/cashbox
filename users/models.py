from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import EmployeeManager
from users.validators import validate_phone


class Employee(AbstractBaseUser, PermissionsMixin):
    """ Пользователь """
    class Role(models.IntegerChoices):
        USER = 0, _('Пользователь')
        CASHIER = 1, _('Кассир')
        DIRECTOR = 2, _('Директор')
        ADMIN = 3, _('Администратор')

    username = None


    phone = models.CharField(max_length=12, unique=True, validators=[validate_phone])
    email = models.EmailField(verbose_name=_('Электронная почта'), blank=True, null=True)
    name = models.CharField(verbose_name=_('Ф.И.О'), max_length=255, null=True, blank=True)
    role = models.IntegerField(verbose_name=_('Рол'), choices=Role.choices, default=Role.USER)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey("common.Organization", on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"