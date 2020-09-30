from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
import os
import requests as python_requests
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from accounts.models import UserProfileInfo, User, Friend
from .models import Post, TagNotification, HashTags, HashTagsPostTable, TaggedPost, Like, Dislike
from .forms import PostForm
from feed.views import feed
from django.http import HttpResponse
from helpers.imgur_client import upload_image
from helpers.youtube_id_parser import video_id
from helpers.spotify_trackid_extractor import get_track_id
from helpers.extract_hashtags import get_hashtags
try:
    from django.utils import simplejson as json
except ImportError:
    import json


@login_required
def create_post(request):
    #print("Cretaing Post")
    user = request.user
    upi = UserProfileInfo.objects.get(user=user)
    if request.method == "POST":
        text = request.POST.get("text")
        from_feed = request.POST.get("from_feed")
        if text == "":
            return feed(request)
        tagged_friends = request.POST.getlist("checkbox_tag")
        try:
            post = Post.objects.create(text=text, author=request.user, author_profile=upi, time_of_posting=timezone.now())
        except Exception as e:
            raise e
        file = None
        try:
            base_url = "https://api.twitter.com/1/statuses/oembed.json?url="
            tweet_url = request.POST.get("tweet_url")
            embed_url = base_url + tweet_url
            embedded_tweet = python_requests.get(embed_url).json()
            embedded_tweet = embedded_tweet['html']
            embedded_tweet = embedded_tweet.split('\n')[0]
            post.tweet_url = embedded_tweet
        except Exception as e:
            print(e)
        try:
            base_url = "https://open.spotify.com/embed/track/"
            spotify_song_url = request.POST.get("spotify_song_url")
            track_id = get_track_id(spotify_song_url)
            spotify_song_url = base_url + track_id
            post.spotify_url = spotify_song_url
        except Exception as e:
            print(e)
        try:
            youtube_video_url = request.POST['youtube_url']
            youtube_video_id = video_id(youtube_video_url).split('&')[0]
            if youtube_video_id:
                default_youtube_embed_url = "https://www.youtube.com/embed/"
                post.youtube_video_url = default_youtube_embed_url + youtube_video_id
                # print(post.youtube_video_url)
        except Exception as e:
            print(e)
        try:
            file = request.FILES['image']
            file, extension = upload_image(file)
            post.imgur_url = file
            post.is_video = extension
            # print("Got the file")
        except Exception as e:
            print(e)
        # post.save()
        for friend in tagged_friends:
            tagged_friend = UserProfileInfo.objects.get(user__username=friend)
            _ = TaggedPost.objects.create(post=post, user=tagged_friend)
            tag_notif = TagNotification.objects.create(post=post, 
                                        tagged_user=tagged_friend.user, time_of_tagging=timezone.now())
        post.save()
        hashtags = get_hashtags(text)
        # print(hashtags)
        for hashtag in hashtags:
            htag = HashTags.objects.get_or_create(keyword=hashtag)[0]
            _ = HashTagsPostTable.objects.create(post=post, hashtag=htag)
    
        if from_feed:
            return JsonResponse({"text":text,
                                 "pk": post.pk,
                                "like_btn_class": "btn-outline-success",
                                "dislike_btn_class" :"btn-outline-danger", 
                                "num_dislikes": 0, 
                                "num_likes": 0})
        return redirect("feed:news_feed")
    else:
        form = PostForm()
        # print("8")
        friends = Friend.objects.filter(source__user=user).annotate(friend_name=F("destination__user__username")
        ).values("friend_name")
        # friends = list(friends)
        return render(request, 'post/new_post.html', {"friends": friends,
                             'friends_exist':friends.exists()})

def view_post(request, post_id):
    post_object = None
    user = request.user
    try:
        post_object = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return render(request, "post/post_not_found.html", {})
    if post_object:
        post = Post.objects.filter(pk=post_id).annotate(
            username=F('author_profile__user__username'), profile_pic_url=F('author_profile__profile_pic_url'), 
            ).values("profile_pic_url", "username", "pk", "text", 
            "time_of_posting", "is_edited", "tweet_url", "spotify_url", "num_likes", "num_dislikes",
            "youtube_video_url", "img_approved", "content_approved", "imgur_url",)
        tagged_users = list()
        post = dict(post[0])
        tagged_users = list(TaggedPost.objects.filter(post=post_object
        ).annotate(username=F('user__user__username')
        ).values("username"))
        post["tags_username"] = tagged_users
        post["liked"] = Like.objects.filter(post=post_object, user__user__username=user.username).exists()
        # print(post["liked"])
        if not post["liked"]:
            post["disliked"] = Dislike.objects.filter(post=post_object, user__user__username=user.username).exists()
        post["hashtags"] = HashTagsPostTable.objects.filter(post=post_object).values("hashtag__keyword")
        current_user = user.username == post["username"]
        return render(request, "post/view_post.html", {"post":post, "current_user":current_user})
    else:
        return render(request, "post/post_not_found.html", {})

@login_required
def edit_post(request, pk):
    print("Edit post")
    try:
        post = Post.objects.get(pk=pk, author=request.user)
        # print("Found post")
    except Post.DoesNotExist:
        return render(request, 'accounts/index.html', {})
    if request.method == "POST":
        text = request.POST.get("text")
        if text == "":
            return feed(request)
        post.text = text
        post.is_edited = True
        post.save()
        hashtags = get_hashtags(text)
        for hashtag in hashtags:
            htag = HashTags.objects.get_or_create(keyword=hashtag)[0]
            _ = HashTagsPostTable.objects.get_or_create(post=post, hashtag=htag)
        return view_post(request, post.pk)
    else:
        form = dict()
        form["text"] = post.text
        form["time"] = post.time_of_posting
        form["tags"] = post.tags.all()
        form["pk"] = pk
        # print(form["tags"])
        return render(request, 'post/edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    print("Delete post")
    try:
        # upi = UserProfileInfo.objects.get(user__username=request.user.username)
        post = Post.objects.get(pk=pk, author_profile__user__username=request.user.username)
        print("Found post")
    except Post.DoesNotExist:
        return render(request, 'accounts/index.html', {})
    if request.method == "POST":
        print("confirmation accepted deleteing.")
        # htag = HashTagsPostTable.filter(post=post)
        post.delete()
    else:
        print("confirm delete")
        post_details = dict()
        post_details["id"] = pk
        return render(request, "post/post_delete_confirmation.html", {"post": post_details})
    return render(request, 'accounts/index.html', {})
        
@login_required
def posts_list(request, author=None):
    current_user = False
    if author is None:
        author = request.user.username
        current_user = True
    # print("Fetching all posts of ", author)
    posts = Post.objects.filter(author__username=author).order_by('-time_of_posting'
                                ).values("text", "pk", "time_of_posting")
    profile_pic_url = UserProfileInfo.objects.get(user__username=author).profile_pic_url
    posts_exist = True
    if not posts:
        posts_exist = False        
    return render(request, "post/posts_list.html", {"posts":posts, "mention":False, 
                                                    "author":author, 
                                                    "posts_exist":posts_exist, 
                                                    "current_user":current_user, 
                                                    "profile_pic_url":profile_pic_url,
                                                     })

@login_required
def filter_posts_hashtag(request, hashtag=None):
    if hashtag is None:
        pass
    hashtags_posts = HashTagsPostTable.objects.filter(hashtag__keyword=hashtag)
    # print(posts[0].post)
    posts = list()
    for post in hashtags_posts:
        posts.append(post.post)
    posts_exist = False
    if posts:
        posts_exist = True
    current_user = True
    profile_pic_url = None
    return render(request, "post/hashtag_filter_posts_list.html", {"posts":posts})

@login_required
def filter_posts_image(request):
    posts = Post.objects.exclude(imgur_url=None).order_by('-time_of_posting'
                                ).values("imgur_url", "pk","is_video")
    # print(posts[0])
    return render(request, "filter_view/image_gallery.html", {"posts":posts, "num_posts":range(0, len(posts), 3)})

@login_required
def filter_posts_spotify(request):
    posts = Post.objects.exclude(spotify_url=None).order_by('-time_of_posting'
                                ).values("spotify_url", "pk")
    return render(request, "filter_view/spotify_gallery.html", {"posts":posts, "num_posts":range(0, len(posts), 3)})

@login_required
def filter_posts_youtube(request):
    posts = Post.objects.exclude(youtube_video_url=None, content_approved=False).order_by('-time_of_posting'
                                ).values("youtube_video_url", "pk")
    return render(request, "filter_view/youtube_gallery.html", {"posts":posts, "num_posts":range(0, len(posts), 3)})


@login_required
def view_mentions(request):
    user = request.user
    print("Fetching mentions ")
    posts = TagNotification.objects.filter(tagged_user=user).order_by('-post__time_of_posting')
    if posts:
        posts = posts.values("post__text","post__pk", "post__author__username",
                                                  "post__time_of_posting")
        print(posts)
        return render(request, "post/posts_list.html", {"posts":posts, "mention":True, "posts_exist":True})
    else:
        return render(request, "post/posts_list.html", {"posts":posts, "mention":True, "posts_exist":False})

@login_required
@require_POST
def like_post(request):
    like_btn_class = None
    dislike_btn_class = None
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(pk=post_id)
        upi = UserProfileInfo.objects.get(user=user)
        like = Like.objects.filter(post=post, user=upi)
        # print(like.exists())
        if like.exists(): 
            like.delete()
            message = "Ummm, I don't know wheteher I like it or not"
            like_btn_class = "btn-outline-success"
            dislike_btn_class = "btn-outline-danger"
            if post.num_likes>0:
                post.num_likes -= 1
        else:
            like_btn_class = "btn-success"
            dislike_btn_class = "btn-outline-danger"
            dislike = Dislike.objects.filter(post=post, user=upi)
            if dislike.exists():
                dislike.delete()
                if post.num_dislikes>0:
                    post.num_dislikes -= 1
            _ = Like.objects.create(post=post, user=upi)
            post.num_likes += 1
            message = "Wow! this one was cool"
        post.save()
    return JsonResponse({"message":message,
                         "like_btn_class": like_btn_class,
                         "dislike_btn_class" :dislike_btn_class, 
                         "num_dislikes": post.num_dislikes, 
                         "num_likes": post.num_likes}) # Sending an success response

@login_required
@require_POST
def dislike_post(request):
    user = request.user
    message = None
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        upi = UserProfileInfo.objects.get(user=user)
        post = Post.objects.get(pk=post_id)
        dislike = Dislike.objects.filter(post=post, user=upi)
        if dislike.exists():
            dislike.delete()
            if post.num_dislikes>0:
                post.num_dislikes -= 1
            message = "Yeah okay, I guess it's not that bad"
            like_btn_class = "btn-outline-success"
            dislike_btn_class = "btn-outline-danger"
        else:
            # add a new like for a post
            like_btn_class = "btn-outline-success"
            dislike_btn_class = "btn-danger"
            _ = Dislike.objects.create(post=post, user=upi)
            post.num_dislikes += 1
            like = Like.objects.filter(post=post, user=upi)
            message = "Nah, I don't like this"
            if like.exists():
                like.delete()
                if post.num_likes>0:
                    post.num_likes -= 1
        post.save()
        num_dislikes = post.num_dislikes
        num_likes = post.num_likes
    return JsonResponse({"message":message,
                         "like_btn_class": like_btn_class,
                         "dislike_btn_class" :dislike_btn_class, 
                         "num_dislikes": num_dislikes, 
                         "num_likes": num_likes}) 



########################################CONTENT##############################################################
@staff_member_required
def get_unapprove_contents(request):
    unapprove = list()
    try:
        content = Post.objects.exclude(youtube_video_url=None
                                ).filter(content_approved=False
                                    ).values("youtube_video_url", "pk")
        for i in content:
            content_link = i["youtube_video_url"] 
            if content_link != "":
                unapprove.append({"content":content_link, "pk":i["pk"]})
    except Exception as e:
        print(e)
    return render(request, 'admin/approve_content.html', {"posts":unapprove})


@staff_member_required
def get_approve_contents(request):
    approve = list()
    try:
        content = Post.objects.exclude(youtube_video_url=None,
                                        ).filter(content_approved=True
                                         ).values("youtube_video_url", "pk")
        for i in content:
            content_link = i["youtube_video_url"] 
            if content_link != "":
                approve.append({"content":content_link, "pk":i["pk"]})
    except Exception as e:
        print(e)
    return render(request, 'admin/approve_content.html', {"posts":approve})

@staff_member_required
def approve_contents(request):
    post_id = request.POST.get("post")
    # print(post_id)
    post = Post.objects.get(pk=post_id)
    post.content_approved = True
    post.save()
    return redirect("post:unapproved_contents")

@staff_member_required
def delete_contents(request):
    post_id = request.POST.get("post")
    print(post_id)
    post = Post.objects.get(pk=post_id)
    post.youtube_video_url = None 
    post.save()
    return redirect("post:unapproved_contents")


########################################IMAGES##############################################################

@staff_member_required
def get_unapprove_images(request):
    unapprove = list()
    try:
        images = Post.objects.exclude(imgur_url=None).filter(img_approved=False).values("imgur_url", "pk")
        for i in images:
            image_link = i["imgur_url"] 
            if image_link != "":
                unapprove.append({"image":image_link, "pk":i["pk"]})
    except Exception as e:
        print(e)
    # print(unapprove)
    return render(request, 'admin/approve.html', {"posts":unapprove})

@staff_member_required
def get_approve_images(request):
    approve = list()
    try:
        images = Post.objects.exclude(imgur_url=None).filter(img_approved=True).values("imgur_url", "pk")
        for i in images:
            image_link = i["imgur_url"] 
            if image_link != "":
                approve.append({"image":image_link, "pk":i["pk"]})
    except Exception as e:
        print(e)
    return render(request, 'admin/approve.html', {"posts":approve})

@staff_member_required
def approve_images(request):
    post_id = request.POST.get("post")
    # print(post_id)
    post = Post.objects.get(pk=post_id)
    post.img_approved = True
    post.save()
    return redirect("post:unapproved")

@staff_member_required
def delete_images(request):
    post_id = request.POST.get("post")
    post = Post.objects.get(pk=post_id)
    post.imgur_url = None 
    post.save()
    return redirect("post:unapproved")