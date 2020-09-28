from django.db import models
from accounts.models import User, UserProfileInfo
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    text = models.TextField(max_length=5000, blank=True)
    author =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    author_profile =  models.ForeignKey(UserProfileInfo, default=None, on_delete=models.CASCADE , related_name="author_profile")
    time_of_posting = models.DateTimeField(blank=True)
    tags = models.ManyToManyField(User, blank=True, related_name="tagged_user")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")
    is_edited = models.BooleanField(default=False)
    imgur_url = models.URLField(default=None, null=True, blank=True)
    img_approved = models.BooleanField(default=False) 
    content_approved = models.BooleanField(default=False) 
    is_video = models.BooleanField(default=False)
    youtube_video_url = models.URLField(default=None, null=True, blank=True)
    tweet_url = models.URLField(default=None, null=True, blank=True)
    spotify_url = models.URLField(default=None, null=True, blank=True)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)

    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()


class TaggedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)


class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)


class TagNotification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tagged_user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_of_tagging = models.DateTimeField(blank=True)
    

class HashTags(models.Model):
    keyword = models.CharField(max_length=30, unique=True)

class HashTagsPostTable(models.Model):
    hashtag = models.ForeignKey(HashTags, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)