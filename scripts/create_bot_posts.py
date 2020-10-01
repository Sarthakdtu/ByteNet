import random
from accounts.models import UserProfileInfo, User, Friend
from post.models import Post, HashTags, HashTagsPostTable, TaggedPost, TagNotification
from scripts.get_reddit_content import *
from django.utils import timezone
from scripts.probability_generator import get_prob
from helpers.link_preview_generator import get_link_preview

def create_bot_posts():
    users = list(UserProfileInfo.objects.filter(is_bot=True))
    nature_tag = HashTags.objects.get(keyword="nature")
    monster_tag = HashTags.objects.get(keyword="monster")
    sky_tag = HashTags.objects.get(keyword="sky")
    house_tag = HashTags.objects.get(keyword="house")
    space_tag = HashTags.objects.get(keyword="space")
    animal_tag = HashTags.objects.get(keyword="animal")
    arch_tag = HashTags.objects.get(keyword="architecture")
    quote_tag = HashTags.objects.get(keyword="quote")
    plant_tag = HashTags.objects.get(keyword="plants")
    bot_tag = HashTags.objects.get(keyword="bot_post")
    # news_tag = HashTags.objects.get(keyword="news")
    til_tag = HashTags.objects.get(keyword="todayilearned")

    quotes = get_quotes()
    til_facts = get_til()
    nature_images = get_earth_images()
    animal_images = get_animal_images()
    sky_images = get_sky_images()
    space_images = get_space_images()
    plant_images = get_plant_images()
    mosnter_images = get_monster_images()
    arch_images = get_arch_images()
    house_images = get_house_images()
    # news = get_news()

    contents = quotes + house_images+ til_facts + nature_images +sky_images +plant_images +animal_images +space_images+mosnter_images+arch_images
    print(len(contents))
    random.shuffle(contents)
    if contents:
        for content in contents:
            if not get_prob():
                continue
            try:
                user = random.choice(users)
                url = content["url"]
                if url:
                    ext = url[-3:]
                    if content["type"]!="news" and ext != "jpg":
                        continue
                approved = content["url"] is not None
                post = Post.objects.filter(text=content["text"])
                if post.exists():
                    print("This post exists")
                    continue
                post = Post.objects.create(author_profile=user, author=user.user, 
                                        text=content["text"], time_of_posting=timezone.now(), 
                                        )
                if content["type"] != "news":
                    post.imgur_url = content["url"]
                    post.img_approved=approved
                else:
                    post.article_link = content["url"]
                    post.article_preview = get_link_preview(content["url"])
                post.save()
                friends = Friend.objects.filter(source=user)
                if friends.exists():
                    friends = list(friends)
                    l = len(friends)
                    friends = random.sample(friends, min(l, 4))
                    for friend in friends:
                        _ = TaggedPost.objects.create(post=post, user=friend.destination)
                        if not friend.destination.is_bot:
                            _ = TagNotification.objects.create(post=post, time_of_tagging=timezone.now() ,tagged_user=friend.destination.user)
                            print("Tagged a real user")
                        print(f"Tagging {friend.destination.user.username}")
                if content["type"] == "q":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=quote_tag)
                if content["type"] == "p":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=plant_tag)
                if content["type"] == "til":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=til_tag)
                if content["type"] == "n":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=nature_tag)
                if content["type"] == "a":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=animal_tag)
                if content["type"] == "s":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=sky_tag)
                if content["type"] == "sp":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=space_tag)
                if content["type"] == "h":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=house_tag)
                if content["type"] == "ar":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=arch_tag)
                if content["type"] == "m":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=monster_tag)
                if content["type"] == "news":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=news_tag)
                _ = HashTagsPostTable.objects.create(post=post, hashtag=bot_tag)
                print("posted ", post.pk)
            except Exception as e:
                print(e)
