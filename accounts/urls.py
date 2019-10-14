from django.conf.urls import url
from accounts import views
app_name = 'accounts'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^delete_account/$', views.delete_account, name='delete_account'),
    url(r'^edit_profile/$', views.edit_account, name='edit_profile'),
       
]