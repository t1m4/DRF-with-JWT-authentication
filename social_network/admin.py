from django.contrib import admin

from social_network.models import Post, Like


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('date', 'time')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
