from accounts.models import UserProfileInfo as upi, User
from post.models import Post, Like, Dislike

posts = Post.objects.all() 

for post in posts:
    try:
        likes = post.likes.values_list("username")
        dislikes = post.dislikes.values_list("username")
        count = 0
        for like in likes:
            count += 1
            like = like[0]
            u = upi.objects.get(user__username=like)
            _ = Like.objects.get_or_create(user=u, post=post)
            print(f"{like} liked post {post.pk}")
        post.num_likes = count
        post.save()
        count = 0
        for like in dislikes:
            count += 1
            like = like[0]
            u = upi.objects.get(user__username=like)
            _ = Dislike.objects.create(user=u, post=post)
            print(f"{like} disliked post {post.pk}")
        post.num_dislikes = count
        post.save()
    except Exception as e:
        print(e)    
        
