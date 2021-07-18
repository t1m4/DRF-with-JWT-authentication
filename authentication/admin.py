from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from authentication.models import User


class MyUserAdmin(UserAdmin):
    readonly_fields = ['date_joined',]
    # add new field 'last_request` in UserAdmin and register it
    UserAdmin.fieldsets[3][1]['fields'] = ('last_login', 'date_joined', 'last_request')


admin.site.register(User, MyUserAdmin)
