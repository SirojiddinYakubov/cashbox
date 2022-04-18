from django.db import models


class BaseModel(models.Model):
    """ Абстрактний базовий модел """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cash(BaseModel):
    """ Абстрактний модель для денежных средств """
    user = models.ForeignKey('users.Employee', on_delete=models.SET_NULL, null=True, related_name="%(class)s_user")
    cashier = models.ForeignKey('users.Employee', on_delete=models.SET_NULL, null=True, related_name="%(class)s_cashier")
    cause = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    payment_type = models.ForeignKey('common.PaymentType', on_delete=models.PROTECT)
    cashbox = models.ForeignKey('common.Cashbox', on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Organization(BaseModel):
    """ Организация """
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Cashbox(BaseModel):
    """ Касса """
    title = models.CharField(max_length=255)
    organization = models.ForeignKey("common.Organization", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Касса"
        verbose_name_plural = "Кассы"


class PaymentType(BaseModel):
    """ Cпособ оплаты """
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Cпособ оплаты"
        verbose_name_plural = "Cпособ оплаты"


class InputCash(Cash):
    """ Ввод денежных средств """

    class Meta:
        verbose_name = "Ввод денежных средств"
        verbose_name_plural = "Ввод денежных средств"


class OutputCash(Cash):
    """ Выход денежных средств """

    class Meta:
        verbose_name = "Выход денежных средств"
        verbose_name_plural = "Выход денежных средств"
