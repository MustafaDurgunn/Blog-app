from django.db import models
# djangonun user modelini cek
from django.contrib.auth.models import User




class TweetLikes(models.Model):

    user = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)
    tweet = models.ForeignKey("user_app.Tweets", verbose_name=("Beğenilen Post"), on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return self.user.username


# Create your models here.
class Tweets(models.Model):

    # tablolalar key/value şeklinde oluşturulur
    # foreignkey tabloları birleştirir, birbirlerine bağlar
    author = models.ForeignKey(User, verbose_name=("Yazar"), on_delete=models.CASCADE)
    tweet = models.TextField(("Tweet içeriği"), max_length=500)
    image = models.FileField(("Dosya"), upload_to="Uploads", blank=True, max_length=100)
    # manytomany 1 den fazla veri kabul eder
    likes = models.ManyToManyField(TweetLikes, verbose_name=("Beğenen Kişiler"), blank=True)
    suspended = models.BooleanField(("Askıda mı"), default=False)
    createdAt = models.DateTimeField(("Oluşturulma Tarihi"), auto_now=True)


    def __str__(self) -> str:
        return self.tweet


class TweetComments(models.Model):

    author = models.ForeignKey(User, verbose_name=("Yorum Yapan"), on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweets, verbose_name=("Tweet"), on_delete=models.CASCADE, related_name="posts")
    message = models.TextField(("Mesaj"), max_length=300)
    # blank true = bu fieldi opsiyonel yap
    image = models.FileField(("Dosya"), upload_to="Comments", max_length=100, blank=True)
    # sadece 1 kişi 1 veriyi tutabilir
    # teketek = models.OneToOneField("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    # admin panelinde object object gözükmemesi icin str veriyorum
    def __str__(self) -> str:
        return self.tweet.tweet


# banlanan userler
class BannedUsers(models.Model):

    authorized = models.ForeignKey(User, verbose_name=("Banlayan"), related_name="yetkililer", on_delete=models.CASCADE)
    suspect = models.ForeignKey(User, verbose_name=("Banlanan"), on_delete=models.CASCADE)
    reason = models.CharField(("Sebep"), max_length=50)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.suspect.username