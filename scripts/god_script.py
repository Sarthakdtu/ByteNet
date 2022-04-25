from scripts.create_bot_users import create_bot_users
from scripts.create_bot_posts import create_bot_posts
from scripts.friend_bot import create_friends
from scripts.like_dislike_function_bots import like_dislike
from scripts.trending_script import trending

def get_this_bread():
    res = ""
    try:
        #res += create_bot_users()
        res += create_bot_posts()
        res += create_friends()
        res += like_dislike()
        res += trending()
    except Exception as e:
        print("Error", e)
        res = str(e)
    return res