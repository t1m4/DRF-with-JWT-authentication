from django.db import models

# Create your models here.
from django.utils import timezone

from authentication.models import User


class Post(models.Model):
    """
    Post in social network
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100000)

class Like(models.Model):
    """
    Like for every post
    """
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='post_likes')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)