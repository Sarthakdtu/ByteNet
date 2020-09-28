from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.models import User, UserProfileInfo, Friend
from constants.constants import FriendRequestStatus
from django.core.paginator import Paginator
from .models import FriendRequest
from post.models import Post, TagNotification, HashTagsPostTable
# Create your views here.

################################## FEED LOGIC  ############################################

@login_required
def feed(request):
    user = request.user
    print("Fetching posts for feed")
    userprofile = UserProfileInfo.objects.all().values_list("profile_pic_url", "user__username")
    profile_pic = dict()
    for i in userprofile:
        profile_pic[i[1]] = i[0]
    posts = Post.objects.all().order_by('-time_of_posting').select_related("author")
    posts_list = list()
    for post in posts:
        post_details = dict()
        username = post.author.username
        post_details["time_of_posting"] = post.time_of_posting
        # print(post.)
        post_details["text"] = post.text
        post_details["is_edited"] = post.is_edited
        post_details["author__username"] = username
        post_details["profile_pic_url"] = profile_pic[username] 
        post_details["tags"] = list(post.tags.all().values("username"))
        post_details["liked"] = post.likes.filter(pk=user.pk).exists()
        post_details["disliked"] = post.dislikes.filter(pk=user.pk).exists() 
        post_details["num_likes"] = post.total_likes()
        post_details["num_dislikes"] = post.total_dislikes()
        post_details["tweet_url"] = post.tweet_url
        post_details["image"] = post.imgur_url
        post_details["is_video"] = post.is_video
        post_details["approved"] = post.img_approved
        post_details["content_approved"] = post.content_approved
        post_details["youtube_url"] = post.youtube_video_url
        post_details["spotify_url"] = post.spotify_url
        post_details["pk"] = post.pk
        hashtags = HashTagsPostTable.objects.filter(post=post).values("hashtag__keyword")
        # print(hashtags)
        post_details["hashtags"] = hashtags
        posts_list.append(post_details)
    paginator = Paginator(posts_list, 20)
    # print(paginator.count, paginator.num_pages)
    page = request.GET.get('page')
    posts_list = paginator.get_page(page)
    return render(request, 'feed/pagination_feed.html', {"posts":posts_list,
     "curr_user_profile_pic":profile_pic[request.user.username]})

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
    #print("Fetching User List For")
    user = request.user
    #print(user.username)
    username = request.user.username
    people_to_be_connected = FriendRequest.objects.filter(source=user,
                                         request_status__in=[FriendRequestStatus.PENDING,
                                                             FriendRequestStatus.DECLINED]
                                                             ).annotate(username=F("destination__user__pk")
                                                             ).values("username")
    people_to_be_connected_list = list()
    for person in list(people_to_be_connected):
        people_to_be_connected_list.append(person["username"])
    people_to_be_connected = FriendRequest.objects.filter(destination=user, 
                                                          request_status=FriendRequestStatus.PENDING
                                                          ).annotate(username=F("source__user__pk")
                                                             ).values("username")
    for person in list(people_to_be_connected):
        people_to_be_connected_list.append(person["username"])
    print("These people are ready to be connected from source side", people_to_be_connected_list)
    people = UserProfileInfo.objects.exclude(friend=user
                                            ).exclude(user__pk__in=people_to_be_connected_list
                                            ).exclude(user=user
                                            ).annotate(username=F('user__username')
                                            ).values("username")
    #print(people)
    people = list(people)
    people = {"people" : people}
    return render(request, 'feed/users_list.html', people)

@login_required
def friends_list(request):
    user = request.user
    print("Fetching friends for ", user.username)
    friends = Friend.objects.filter(source__user=user).annotate(
        username=F('destination__user__username')).values("username")
    # friends = UserProfileInfo.objects.filter(user=user,
                                    # )
    friends_list = list(friends)
    friends = {"friends":friends_list}
    #print(friends)
    friends_exist = True
    if not friends:
        friends_exist = False
    print(friends_exist)
    friends["friends_exist"] = friends_exist
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
    print(sent_requests)
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
            friend = FriendRequest.objects.get(source=destination, destination=source)
        except FriendRequest.DoesNotExist:
            friend = FriendRequest()
        friend.source = source
        friend.destination = destination
        friend.request_status = FriendRequestStatus.PENDING
        friend.save()
        print("Request Sent")
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
            profile = UserProfileInfo.objects.get(user=source)
            profile.friend.add(destination)
            profile.num_friends = profile.num_friends + 1
            profile.save()
            profile = UserProfileInfo.objects.get(user=destination)
            profile.friend.add(source)
            profile.num_friends = profile.num_friends + 1
            profile.save()
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

##################################### HANDLING ERRORS #################################################
#TODO
############################################################################################