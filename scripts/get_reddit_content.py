import praw
from scripts.reddit_secret import *

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, 
                    client_secret=REDDIT_CLIENT_SECRET, 
                    user_agent=REDDIT_APP_NAME, 
                    username=REDDIT_USERNAME,
                    password=REDDIT_PASSWORD)


def get_earth_images():
    subreddit = reddit.subreddit('EarthPorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"n"})
    return images


def get_plant_images():
    subreddit = reddit.subreddit('BotanicalPorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"p"})
    return images


def get_animal_images():
    subreddit = reddit.subreddit('eyebleach')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"a"})
    return images


def get_sky_images():
    subreddit = reddit.subreddit('SkyPorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"s"})
    return images


def get_space_images():
    subreddit = reddit.subreddit('SpacePorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"sp"})
    return images

def get_quotes():
    quotes = None
    try:
        quotes = list()
        subreddit = reddit.subreddit('quotes')
        top_subreddit = subreddit.hot(limit = 20)
        for post in top_subreddit:
            quotes.append({"text":post.title, "url":None, "type":"q"})
    except Exception as e:
        pass
    return quotes


def get_til():
    til_facts = None
    try:
        til_facts = list()
        subreddit = reddit.subreddit('todayilearned')
        top_subreddit = subreddit.hot(limit = 20)
        for post in top_subreddit:
            til_facts.append({"text":post.title, "url":None, "type":"til"})
    except Exception as e:
        pass
    return til_facts


def get_house_images():
    subreddit = reddit.subreddit('HousePorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"h"})
    return images


def get_arch_images():
    subreddit = reddit.subreddit('ArchitecturePorn')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"ar"})
    return images


def get_monster_images():
    subreddit = reddit.subreddit('ImaginaryMonsters')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    images = list()
    for post in posts:
        images.append({"url":post.url, "text":post.title, "type":"m"})
    return images

def get_news():
    subreddit = reddit.subreddit('news')
    top_subreddit = subreddit.hot(limit = 10)
    posts = [i for i in top_subreddit]
    links = list()
    for post in posts:
        links.append({"url":post.url, "text":post.title, "type":"news"})
    return links