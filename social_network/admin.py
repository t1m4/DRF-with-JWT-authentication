from django.contrib import admin

from social_network.models import Post, Like


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'create_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
