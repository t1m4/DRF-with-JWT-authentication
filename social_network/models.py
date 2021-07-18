from django.db import models

from authentication.models import User


# Create your models here.


class Post(models.Model):
    """
    Post in social network
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)

    def __str__(self):
        return "{}-{}".format(self.user, self.title)


class Like(models.Model):
    """
    Like for every post
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return "{}-{}".format(self.user, self.post)