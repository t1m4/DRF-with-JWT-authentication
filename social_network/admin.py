from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from social_network.models import Post, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time')
    list_filter = ('date', )
    search_fields = ('date',    'time')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)