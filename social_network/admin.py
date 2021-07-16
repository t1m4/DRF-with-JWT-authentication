from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _

# from authentication.models import User

# class MyUserAdmin(UserAdmin):
# # class MyUserAdmin(admin.ModelAdmin):
#     readonly_fields = ['date_joined',]
#     UserAdmin.fieldsets[3][1]['fields'] = ('last_login', 'date_joined', 'last_request')


# add new field 'last_request` in UserAdmin and register it
from social_network.models import User

admin.site.register(User)
