import re

def get_hashtags(text):
    regex = r"#(\w+)"
    hashtags = re.findall(regex, text)
    return hashtags
