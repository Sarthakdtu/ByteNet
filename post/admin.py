from django.contrib import admin
from post.models import Post, TagNotification, HashTags, HashTagsPostTable, Like, Dislike, TaggedPost
# Register your models here.
admin.site.register(Post)
admin.site.register(TagNotification)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(HashTagsPostTable)
admin.site.register(HashTags)
admin.site.register(TaggedPost)