from django.conf.urls import url
from accounts import views
from django.urls import path
from post import views
app_name = 'post'

urlpatterns = [
    url(r'^create_post/$', views.create_post, name='create_post'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    
    url(r'^posts_list/$', views.posts_list, name='posts_list'),
    url(r'^mentioned_posts/$', views.view_mentions, name='view_mentions'),
    url(r'^like_post/$', views.like_post , name='like_post'),
    url(r'^dislike_post/$', views.dislike_post , name='dislike_post'),

    
    path('view_post/<int:post_id>/', views.view_post, name='view_post'),
    path('posts_list/<slug:author>/', views.posts_list, name='posts_list'),
]