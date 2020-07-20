from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Used for translations (just like wordpress)
from django.utils.translation import gettext as _
from core import models


# Inherite from Django's default UserAdmin
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    # Fieldset tuples are ('Section title' , {'fields': ('field_one', 'field_two')})
    # IMPORTANT: Adding just 1 item in the 'fields' value tuple you need to add a comma!
    fieldsets = (
        # The top section
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Docs: https://docs.djangoproject.com/en/2.2/topics/auth/customizing
    # IMPORTANT: Adding just 1 item in the 'fields' value tuple you need to add a comma!
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.Tag)
admin.site.register(models.User, UserAdmin)
