from post.models import Trending, Post, HashTags, HashTagsPostTable
from datetime import timedelta
from django.utils import timezone

def trending():
    try:
        curr = Trending.objects.all().delete()
    except Exception as e:
        print(e)

    posts = Post.objects.filter(time_of_posting__gte=timezone.datetime.today() - timedelta(1))
    hashtags = HashTagsPostTable.objects.filter(post__in=posts).exclude(hashtag__keyword="bot_post").values_list("hashtag__keyword")
    trend = dict()
    for tag in hashtags:
        tag = tag[0]
        if tag in trend:
            trend[tag] +=1
        else:
            trend[tag] = 1
    trend_list = list()
    for t in trend:
        trend_list.append([t, trend[t]])
    trend_list = sorted(trend_list,key=lambda x: x[1])
    trend_list.reverse()
    trend_list = trend_list[:min(5, len(trend_list))]

    for t in trend_list:
        print(t[0], " is trending with ", t[1], "posts.")
        t = t[0]
        tag = HashTags.objects.get(keyword=t)
        _ = Trending.objects.create(hashtag=tag)
    
    return "Trending "