def like_dislike():
    from post.models import Like, Dislike, Post
    from accounts.models import UserProfileInfo
    from scripts.probability_generator import get_prob
    import random
    likes_number = 0
    dislikes_number = 0
    posts = Post.objects.filter(author_profile__is_bot=True)
    users = list(UserProfileInfo.objects.filter(is_bot=True))
    for post in posts:
        user = random.choice(users)
        if Like.objects.filter(post=post, user=user).exists() or Dislike.objects.filter(post=post, user=user):
            continue
        if not get_prob():
            _ = Like.objects.get_or_create(user=user, post=post)
            post.num_likes += 1
            post.save()
            likes_number += 1
        else:
            if get_prob():
                if not get_prob():
                    _ = Dislike.objects.get_or_create(user=user, post=post)
                    post.num_dislikes += 1
                    post.save()
                    dislikes_number += 1
    return " Likes and Dislikes " + str(likes_number) + " " +str(dislikes_number)