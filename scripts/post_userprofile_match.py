
from django.db.models import F
from accounts.models import UserProfileInfo as upi, User
from post.models import Post

posts = Post.objects.all()

for post in posts:
        print("--------------------------------------------------------------------------")
        print("Working on post ", post.pk)
        try:
                profile = upi.objects.get(user=post.author)
                # res = upi.objects.filter(user=user).annotate(username=F('friend__username')).values("username")
                post.user_profile = profile
                post.save()
        except Exception as e:
                print(e)
                continue
