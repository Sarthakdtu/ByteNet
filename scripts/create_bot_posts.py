import random
from accounts.models import UserProfileInfo, User
from post.models import Post, HashTags, HashTagsPostTable
from scripts.get_reddit_content import *
from django.utils import timezone
from scripts.probability_generator import get_prob

def create_bot_posts():
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
    til_tag = HashTags.objects.get(keyword="todayilearned")

    users = list(UserProfileInfo.objects.filter(is_bot=True))

    # users = random.sample(users, 10)
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
                    if ext != "jpg":
                        continue
                approved = content["url"] is not None
                post = Post.objects.filter(text=content["text"])
                if post.exists():
                    print("This post exists")
                    continue
                post = Post.objects.create(author_profile=user, author=user.user, 
                                        text=content["text"], time_of_posting=timezone.now(), 
                                        img_approved=approved, imgur_url=content["url"])

                if content["type"] == "q":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=quote_tag)
                if content["type"] == "p":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=plant_tag)
                if content["type"] == "n":
                    _ = HashTagsPostTable.objects.create(post=post, hashtag=til_tag)
                if content["type"] == "til":
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
                _ = HashTagsPostTable.objects.create(post=post, hashtag=bot_tag)
                print("posted ", post.pk)
            except Exception as e:
                print(e)
