
def create_friends():
    from accounts.models import Friend, UserProfileInfo
    from scripts.probability_generator import get_prob
    from feed.models import FriendRequest, FriendRequestStatus
    import random
    users = list(UserProfileInfo.objects.filter(is_bot=True))
    for user in users:
        if get_prob():
            continue
        friend_req = FriendRequest.objects.filter(destination=user.user)
        if friend_req.exists():
            for req in friend_req:
                if not get_prob():
                    continue
                prof = UserProfileInfo.objects.get(user=req.source)
                _ = Friend.objects.get_or_create(source=user, destination=prof)
                _ = Friend.objects.get_or_create(source=prof, destination=user)
                print("Request Accepted")
                req.delete()
        if not get_prob() and get_prob():
            continue
        friend = random.choice(users)
        if friend == user:
            continue
        _ = Friend.objects.get_or_create(source=user, destination=friend)
        _ = Friend.objects.get_or_create(source=friend, destination=user)
        print(f"{user.user.username} is now a friend of {friend.user.username}.")
        