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

    path('unapproved_images/', views.get_unapprove_images, name='unapproved'),
    path('approved_images/', views.get_approve_images, name='approved'),
    path('review_images/', views.approve_images, name='review'),
    path('delete_images/', views.delete_images, name='delete'),


    path('unapproved_contents/', views.get_unapprove_contents, name='unapproved_contents'),
    path('approved_contents/', views.get_approve_contents , name='approved_contents'),
    path('review_contents/', views.approve_contents, name='review_contents'),
    path('delete_contents/', views.delete_contents, name='delete_contents'),

]