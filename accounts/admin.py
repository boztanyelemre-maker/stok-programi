from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_approved', 'is_active']
    list_filter = ['role', 'is_approved', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('role', 'tc_kimlik', 'phone', 'work_phone',
                                     'company', 'authorized_name', 'authorized_surname',
                                     'country', 'city', 'district', 'title',
                                     'is_approved', 'projects')}),
    )
