from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom field heading',
            {
                'fields':(
                    'is_customer',
                    'is_engineer'
                )
            }
        )
    )
admin.site.register(User, CustomUserAdmin)