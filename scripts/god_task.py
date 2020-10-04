from scripts.create_bot_users import create_bot_users
from scripts.create_bot_posts import create_bot_posts
from scripts.friend_bot import create_friends
from scripts.like_dislike_function_bots import like_dislike
from scripts.trending_script import trending

res = ""
res += create_bot_posts()
print(res)
res += like_dislike()
print(res)
res += trending()
print(res)
