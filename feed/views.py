from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import User, UserProfileInfo, Friend
from constants.constants import FriendRequestStatus
from django.core.paginator import Paginator
from .models import FriendRequest
from post.models import Post, TagNotification, HashTagsPostTable, Like, TaggedPost, Dislike
# Create your views here.

################################## FEED LOGIC  ############################################

@login_required
def feed(request):
    user = request.user
    pfp = UserProfileInfo.objects.get(user=user).profile_pic_url
    posts = Post.objects.all().order_by('-time_of_posting'
                        ).select_related("author_profile"
                        ).annotate(username=F('author_profile__user__username'
                                            ), profile_pic_url=F('author_profile__profile_pic_url'), 
                        ).values("profile_pic_url", "username", "pk", "text", "time_of_posting", "is_video",
                                "is_edited", "tweet_url", "spotify_url", "num_likes", "num_dislikes", 
                                "youtube_video_url", "img_approved", "content_approved", "imgur_url","article_preview")
    posts_list = list()
    for post in posts:
        post["liked"] = Like.objects.filter(post__pk=post["pk"], user__user__username=user.username).exists()
        if not post["liked"]:
            post["disliked"] = Dislike.objects.filter(post__pk=post["pk"], user__user__username=user.username).exists()
        hashtags = HashTagsPostTable.objects.filter(post__pk=post["pk"]).values("hashtag__keyword")
        post["hashtags"] = hashtags
        post["tags"] = TaggedPost.objects.filter(post__pk=post["pk"]
                                    ).annotate(username=F('user__user__username')
                                    ).values("username")
    paginator = Paginator(posts, 30)
    page = request.GET.get('page')
    posts_list = paginator.get_page(page)
    return render(request, 'feed/pagination_feed.html', {"posts":posts_list,
     "curr_user_profile_pic":pfp})

@login_required
def view_profile(request, profile_username=None):
    user_profile = {'current_user':False}
    if profile_username is None:
        profile_username = User.objects.get(username=request.user)
        user_profile = {'current_user':True}
    print(f"{request.user} is about to view {profile_username}'s profile'")
    profile = UserProfileInfo.objects.get(user__username=profile_username)
    user_profile['username'] = profile_username
    try:
        user_profile['age'] = profile.age
        user_profile['profile_pic_url'] = profile.profile_pic_url
    except:
        pass
    try:
        user_profile['location'] = profile.location
    except:
        pass
    try:
        user_profile['email'] = profile.user.email
    except:
        pass
    try:
        user_profile['user'] = profile.user
    except:
        pass
    user_profile['name'] = profile.user.first_name + " " + profile.user.last_name
    user_profile['friend'] = True
    return render(request, 'feed/profile_info.html', user_profile)


######################################## FRIEND LOGIC  ############################################

@login_required
def find_friends(request):
    user = request.user
    username = user.username
    people_to_be_connected1 = FriendRequest.objects.filter(source=user,
                                         request_status__in=[FriendRequestStatus.DECLINED, FriendRequestStatus.PENDING]
                                                             ).annotate(pk=F("destination__pk")
                                                             ).values_list("pk", flat=True)
    
    people_to_be_connected1 = list(people_to_be_connected1)
    people_to_be_connected2 = FriendRequest.objects.filter(destination=user, 
                                                          request_status=FriendRequestStatus.PENDING
                                                          ).annotate(pk=F("source__pk")
                                                             ).values_list("pk", flat=True)
    people_to_be_connected2 = list(people_to_be_connected2)
    friends = Friend.objects.filter(source__user=user).annotate(pk=F("destination__user__pk")).values_list('pk', flat=True)
    
    people = UserProfileInfo.objects.exclude(user__pk__in=people_to_be_connected1
                                            ).exclude(user__pk__in=people_to_be_connected2
                                            ).exclude(user__pk__in=friends
                                            ).exclude(user=user
                                            ).annotate(username=F('user__username'),pk=F("user__pk"), 
                                            first_name=F('user__first_name'), last_name=F('user__last_name')
                                            ).values("username", "profile_pic_url", "first_name", "last_name", "pk")   
    people = list(people)
    people = {"people" : people, "range":range(0, len(people), 3)}
    return render(request, 'feed/users_list.html', people)

@login_required
def friends_list(request, username=None):
    user = None
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user
    friends = Friend.objects.filter(source__user=user).annotate(
        first_name=F('destination__user__first_name'),
        last_name=F('destination__user__last_name'),
        profile_pic_url=F("destination__profile_pic_url"),
        username=F('destination__user__username')).values("username", "profile_pic_url", "first_name", "last_name")
    friends_list = list(friends)
    friends = {"friends":friends_list}
    friends_exist = True
    if not friends:
        friends_exist = False
    friends["friends_exist"] = friends_exist
    friends["range"] = range(0, min(len(friends_list), 100), 3)
    return render(request, "feed/friends_list.html",friends )
    
################################## FRIEND REQUESTS LIST ###########################################

@login_required
def pending_friend_requests(request):
    user = request.user
    show = True
    print("Fetching pending friend requests for ", user)
    pending_requests = FriendRequest.objects.filter(destination=user,
                                             request_status=FriendRequestStatus.PENDING
                                    ).annotate(username=F('source__username')).values("username")
    if not pending_requests:
        show = False
    # print(pending_requests)
    pending_requests = {"pending_requests": list(pending_requests), "pending":True, "sent":False, "show":show}
    return render(request, "feed/friend_requests_list.html", pending_requests)

@login_required
def sent_friend_requests(request):
    print("Fetching sent friend requests")
    user = request.user
    show = True
    sent_requests = FriendRequest.objects.filter(source=user,
                                          request_status__in=[FriendRequestStatus.PENDING, 
                                          FriendRequestStatus.DECLINED]
                                          ).annotate(friend__username=F("destination__username")
                                          ).values("friend__username")
    # print(sent_requests)
    if not sent_requests:
         show = False
    sent_requests = {"sent_requests": list(sent_requests), "pending":False, "sent":True, "show":show}
    return render(request, "feed/friend_requests_list.html", sent_requests)

########################################### FRIEND REQUEST ACCEPTANCE/REJECTION  ##########################################
@login_required
def send_friend_request(request):
    if request.method == "POST":
        source = request.user
        destination = request.POST.get("username")
        destination = User.objects.get(username=destination)
        print(f"{source} has send a friend request to {destination}")
        try:
            friend = FriendRequest.objects.get(source=source, destination=destination)
            # print("exists")
        except FriendRequest.DoesNotExist:
            friend = FriendRequest()
            friend.source = source
            friend.destination = destination
            friend.request_status = FriendRequestStatus.PENDING
            friend.save()
            # print("Request Sent")
        return render(request, "feed/request_sent_success.html", {"destination":destination})

@login_required
def accept_friend_request(request):
    if request.method == "POST":
        print("Accepting request")
        source = request.POST.get("accept_request")
        source = User.objects.get(username=source)
        destination = request.user
        print(f"{destination.username} is accepting friend request from {source.username}")
        try:
            friend_request = FriendRequest.objects.get(source=source, destination=destination)
            source_profile = UserProfileInfo.objects.get(user=source)
            destination_profile = UserProfileInfo.objects.get(user=destination)
            f1 = Friend.objects.create(source=source_profile, destination=destination_profile)
            f1 = Friend.objects.create(destination=source_profile, source=destination_profile)
            source_profile.num_friends = source_profile.num_friends + 1
            source_profile.save()
            destination_profile.num_friends = destination_profile.num_friends + 1
            destination_profile.save()
            friend_request.delete()
            print(f"{source} and {destination} are now friends.")
            return render(request, "feed/friend_success.html", {"destination": source.username})
        except FriendRequest.DoesNotExist:
            print("Invalid friend request acception")
        
@login_required
def decline_friend_request(request):
     if request.method == "POST":
        #print("Declining a friend request")
        source = request.POST.get("decline_request")
        print(source)   
        source = User.objects.get(username=source)
        destination = request.user
        print(f"{destination.username} is declining friend request from {source.username},")
        friend_request = FriendRequest.objects.get(source=source, destination=destination)
        friend_request.request_status = FriendRequestStatus.DECLINED
        friend_request.save()
        print("Friend request declined.")
        return pending_friend_requests(request)



##################################### SEARCH LOGIC###################################
@login_required
def search(request):
    keyword = request.GET.get('keyword')
    users = User.objects.filter(Q(username__contains=keyword) |
                                Q(first_name__icontains=keyword) |
                                Q(last_name__icontains=keyword)).values("username")
    user_exist = True
    if not users:
        user_exist = False
    users = list(users)
    users = {"users":users}
    
    users["user_exist"] = user_exist
    users["keyword"] = keyword
    return render(request, "feed/search_list.html", users )

@staff_member_required
def get_not_bots(request):
    people = UserProfileInfo.objects.exclude(is_bot=True
                                            ).annotate(username=F('user__username'), 
                                            first_name=F('user__first_name'),
                                            last_name=F('user__last_name')
                                            ).values("username",
                                             "profile_pic_url", "first_name", "last_name")   
    people = list(people)
    people = {"people" : people, "range":range(0, len(people), 3)}
    return render(request, 'feed/users_list.html', people)

##################################### HANDLING ERRORS #################################################
#TODO
############################################################################################