from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Tweets)
admin.site.register(TweetComments)
admin.site.register(TweetLikes)
admin.site.register(BannedUsers)