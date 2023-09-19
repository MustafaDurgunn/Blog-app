"""
URL configuration for blogApp_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# url image, video configuration
from django.conf import settings
from django.conf.urls.static import static


# site appın viewlerini çek
from site_app.views import *
# user_appin viewlerini çek
from user_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="home"),

    # profil endpoint
    path("profil/<userId>", userProfile, name="user-profile"),
    path("profil/<userId>/ban", banUser, name="ban-profile"),
    path("profil/<userId>/unban", unbanUser, name="unban-profile"),


    path("tweets/<tweetId>", tweetDetail, name="tweet-detail"),
    path("tweets/<tweetId>/delete", deleteTweet, name="tweet-delete"),
    path("tweets/<tweetId>/update", updateTweet, name="tweet-update"),

    # yorum endpoint
    path("tweets/<tweetId>/create/comment", createComment, name="create-comment" ),
    path("tweets/<commentId>/delete/comment", deleteComment, name="delete-comment" ),

    path("giris", giris_yap, name="login"),
    path('kayit-ol', kayit_ol, name="register"),
    path('cikis', cikis_yap, name="logout"),

    # hata 
    path("404", notFound, name="404"),

    # api
    path("api/v1/tweets/<tweetId>/like", likeTweet, name="like-tweet" ),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
