from django.db import models
from constants.constants import FriendRequestStatus
from accounts.models import User

# Create your models here.

class FriendRequest(models.Model):
    SOURCE_CHOICES = (
        (FriendRequestStatus.DECLINED, 'declined'),
        (FriendRequestStatus.PENDING, 'pending'),
        (FriendRequestStatus.BLOCKED, 'blocked'),)

    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destination')

    request_status = models.CharField(max_length=30, choices=((FriendRequestStatus.DECLINED, 'declined'),
        (FriendRequestStatus.PENDING, 'pending'),
        (FriendRequestStatus.BLOCKED, 'blocked')), db_index=True)
