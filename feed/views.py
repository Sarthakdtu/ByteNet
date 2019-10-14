from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.models import User, UserProfileInfo
from constants.constants import FriendRequestStatus

from .models import FriendRequest
from post.models import Post, TagNotification
# Create your views here.

###########################################   FEED LOGIC  ############################################

@login_required
def feed(request):
    user = request.user
    print("Fetching posts for feed")
    posts = Post.objects.all().order_by('-time_of_posting').select_related("author")
    posts_list = list()
    for post in posts:
        post_details = dict()
        post_details["time_of_posting"] = post.time_of_posting
        post_details["text"] = post.text
        post_details["is_edited"] = post.is_edited
        post_details["author__username"] = post.author.username
        post_details["tags"] = list(post.tags.all().values("username"))
        post_details["liked"] = post.likes.filter(pk=user.pk).exists()
        post_details["disliked"] = post.dislikes.filter(pk=user.pk).exists() 
        post_details["num_likes"] = post.total_likes()
        post_details["num_dislikes"] = post.total_dislikes()
        #print("is", post_details["liked"])
        #print("Dis", post_details["disliked"])
        post_details["pk"] = post.pk
        posts_list.append(post_details)

    return render(request, 'feed/feed.html', {"posts":list(posts_list)})

@login_required
def view_profile(request, profile_username=None):
    user_profile = {'current_user':False}
    if profile_username is None:
        profile_username = User.objects.get(username=request.user)
        user_profile = {'current_user':True}
    #print(f"{request.user} is about to view {profile_username}'s profile'")
    profile = UserProfileInfo.objects.get(user__username=profile_username)
    user_profile['username'] = profile_username
    user_profile['age'] = profile.age
    user_profile['location'] = profile.location
    user_profile['email'] = profile.user.email
    user_profile['user'] = profile.user
    user_profile['name'] = profile.user.first_name + " " + profile.user.last_name
    user_profile['friend'] = True#profile.friend.filter(username=profile_username).exists()
    #friend_requestFriendRequest.objects.filter(Q(source=user_profile['username']) | Q(destination=user_profile['username']))
    #print(user_profile['friend'])
    #print("If Does not exist error occurs it might be because of incomplete info")
    #print(user_profile)
    return render(request, 'feed/profile_info.html', user_profile)


###########################################   FRIEND LOGIC  ############################################

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
    #print("These people are ready to be connected from source side", people_to_be_connected_list)
    people_to_be_connected = FriendRequest.objects.filter(destination=user, 
                                                          request_status=FriendRequestStatus.PENDING
                                                          ).annotate(username=F("source__user__pk")
                                                             ).values("username")
    for person in list(people_to_be_connected):
        people_to_be_connected_list.append(person["username"])
    #print("These people are ready to be connected from source side", people_to_be_connected_list)
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
    friends = UserProfileInfo.objects.filter(user=user,
                                    ).annotate(username=F('friend__username')).values("username")
    friends_list = list(friends)
    friends = {"friends":friends_list}
    print(friends)
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

##################################### HANDLING ERRORS #################################################
#TODO
############################################################################################



