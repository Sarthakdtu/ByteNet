from accounts.models import UserProfileInfo as upi, User
from post.models import Post, TaggedPost

posts = Post.objects.all() 

for post in posts:
    try:
        tags = post.tags.values_list("username")
        # dislikes = post.dislikes.values_list("username")
        # count = 0
        for tag in tags:
            count += 1
            tag = tag[0]
            u = upi.objects.get(user__username=tag)
            _ = TaggedPost.objects.create(user=u, post=post)
            print(f"{tag} tagged in post {post.pk}")
        
    except Exception as e:
        print(e)    
        
