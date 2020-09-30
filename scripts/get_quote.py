import praw
from scripts.reddit_secret import *
# import random

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, 
                    client_secret=REDDIT_CLIENT_SECRET, 
                    user_agent=REDDIT_APP_NAME, 
                    username=REDDIT_USERNAME,
                    password=REDDIT_PASSWORD)

def generate_text():
    quotes = None
    try:
        subreddit = reddit.subreddit('quotes')
        top_subreddit = subreddit.hot(limit = 20)
        quotes = [i.title for i in top_subreddit]
    except Exception as e:
        pass
    return quotes