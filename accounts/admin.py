from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MasterProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role', 'full_name', 'phone', 'must_change_password')}),
    )


@admin.register(MasterProfile)
class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years')
