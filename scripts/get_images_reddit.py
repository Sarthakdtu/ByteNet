# import praw, requests
# from scripts.reddit_secret import *
# # import random

# reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, 
#                     client_secret=REDDIT_CLIENT_SECRET, 
#                     user_agent=REDDIT_APP_NAME, 
#                     username=REDDIT_USERNAME,
#                     password=REDDIT_PASSWORD)

# # def generate_text():
# #     posts = None
# #     try:
# #         subreddit = reddit.subreddit('EarthPorn')
# #         top_subreddit = subreddit.hot(limit = 20)
# #         posts = [i.title for i in top_subreddit]
# #     except Exception as e:
# #         pass
# #     return posts
# subreddit = reddit.subreddit('EarthPorn')
# top_subreddit = subreddit.hot(limit = 2)
# posts = [i for i in top_subreddit]
# url_id = str(posts[0])
# url = f"https://www.reddit.com/{url_id}/.json"
# res = requests.get(url).json()
# print(res)
# print(res['data']['children'][0]['data']['url'])