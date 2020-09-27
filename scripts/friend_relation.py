
from django.db.models import F
from accounts.models import UserProfileInfo as upi, User, Friends

users = User.objects.all()

for user in users:
        print("--------------------------------------------------------------------------")
        print("Working on user ", user)
        try:
                profile = upi.objects.get(user=user)
                res = upi.objects.filter(user=user).annotate(username=F('friend__username')).values("username")
                for f in res:
                        fr = upi.objects.get(user__username=f['username'])
                        print(f"Making {fr.user.username} and {profile.user.username} friends.")
                        op = Friends.objects.create(source=profile, destination=fr)
                        op.save()
                        print(op.pk)
                        # if len(op)==0:
                        #         continue
                        # print(op)
                        # op[0].delete()
                        # op[1].delete()
                        # print(op)
        except Exception as e:
                print(e)
                continue
