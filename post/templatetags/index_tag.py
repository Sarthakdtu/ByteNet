from django import template
register = template.Library()

@register.filter
def index(posts, i):
    post_list = list()
    size = len(posts)
    post_list.append(posts[i])
    if i+1<size:
        post_list.append(posts[i+1])
    if i+2<size:
        post_list.append(posts[i+2])
    return post_list