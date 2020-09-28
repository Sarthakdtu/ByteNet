from django.contrib import admin
from accounts.models import UserProfileInfo, User, Friend
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Friend)