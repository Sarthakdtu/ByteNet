
def create_bot_users():
    from accounts.models import User, UserProfileInfo as upi, Friend
    from scripts.generate_user import get_random_user
    for i in range(0, 10):
        user = get_random_user()
        if user:
            new_user = User.objects.create(username=user["username"], email=user["email"], 
                                            first_name=user["first"],
                                            last_name=user["last"]
                                            )
            new_user.set_password(user["password"])
            new_user.save()
            profile = upi.objects.create(user=new_user, age=user["age"], location=user["location"], 
                                            profile_pic_url=user["profile_pic_url"], is_bot=True)
            print("User created with username ", user["username"])