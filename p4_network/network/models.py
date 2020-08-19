from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=240, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    lastEdit = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User,  blank=True, related_name='likeUser')
    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name='followersUser')
    following = models.ManyToManyField(User, blank=True, related_name='followingUser')
    def __str__(self):
        return self.user.username
