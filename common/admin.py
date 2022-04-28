from django.contrib import admin
from common.models import (InputCash, OutputCash, Organization, Cashbox, PaymentType)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title', ]
    search_fields = ['title']
    save_on_top = True

@admin.register(InputCash)
class InputCashAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cashier', 'is_active',
                    'cause', 'amount', 'payment_type', 'cashbox']
    list_display_links = ['user', 'cashier', ]
    list_filter = ['payment_type', 'is_active', ]
    search_fields = ['cause', 'amount']
    save_on_top = True


@admin.register(OutputCash)
class OutputCashAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cashier', 'is_active',
                    'cause', 'amount', 'payment_type', 'cashbox']
    list_display_links = ['user', 'cashier', ]
    list_filter = ['payment_type', 'is_active', ]
    search_fields = ['cause', 'amount']
    save_on_top = True