from accounts.models import UserProfileInfo, User
from post.models import Post, HashTags, HashTagsPostTable
from scripts.get_quote import generate_text
from scripts.get_til_facts import generate_til
from django.utils import timezone
import random
quote_tag = HashTags.objects.get(keyword="quote")
bot_tag = HashTags.objects.get(keyword="bot_post")
til_tag = HashTags.objects.get(keyword="todayilearned")
users = list(UserProfileInfo.objects.filter(is_bot=True))
content = generate_text()
if content:
    for text in content:
        user = random.choice(users)
        post = Post.objects.create(author_profile=user, author=user.user, 
                                text=text, time_of_posting=timezone.now())
        _ = HashTagsPostTable.objects.create(post=post, hashtag=quote_tag)
        _ = HashTagsPostTable.objects.create(post=post, hashtag=bot_tag)
#         print(post.text)

content = generate_til()
if content:
    for text in content:
        user = random.choice(users)
        post = Post.objects.create(author_profile=user, author=user.user, 
                                text=text, time_of_posting=timezone.now())
        _ = HashTagsPostTable.objects.create(post=post, hashtag=til_tag)
        _ = HashTagsPostTable.objects.create(post=post, hashtag=bot_tag)
        # print(post.text)
# for user in users: