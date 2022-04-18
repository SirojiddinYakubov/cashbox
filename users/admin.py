from django.contrib import admin
from django.contrib.auth import get_user_model

Employee = get_user_model()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'name', 'is_active',
                    'is_superuser', 'is_staff', 'date_joined', 'last_login']
    list_display_links = ['role', 'name', ]
    list_filter = ['role', 'is_active', ]
    search_fields = ['name', 'phone']
    save_on_top = True
