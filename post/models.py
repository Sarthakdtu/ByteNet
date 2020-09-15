from django.db import models
from accounts.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    text = models.TextField(max_length=500, blank=True)
    author =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    time_of_posting = models.DateTimeField(blank=True)
    tags = models.ManyToManyField(User, blank=True, related_name="tagged_user")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")
    is_edited = models.BooleanField(default=False)
    imgur_url = models.URLField(default=None, null=True)
    img_approved = models.BooleanField(default=False) 
    content_approved = models.BooleanField(default=False) 
    is_video = models.BooleanField(default=False)
    youtube_video_url = models.URLField(default=None, null=True)

    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()

class TagNotification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tagged_user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_tagging = models.DateTimeField(blank=True)
    
