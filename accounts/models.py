from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    location = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True, default=13)
    friend = models.ManyToManyField(User, blank=True, related_name='friend')
    follower = models.ManyToManyField(User, blank=True, related_name='follower')
    num_friends = models.IntegerField(default=0)
    num_followers = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

