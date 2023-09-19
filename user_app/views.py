from django.shortcuts import render, redirect

# djangonun user modelini dahil et
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from .models import *
from site_app.form import CreateTweet, CreateComment

# userappdaki formu al
from .form import UpdateUser


# message frameworku (flash messages)
from django.contrib import messages
# JSON Response
from django.http import JsonResponse

# Create your views here.
def giris_yap(request):

    if request.method == 'POST':
         
         k_adi = request.POST.get('k_adi')
         k_sifre = request.POST.get('k_sifre')

         if k_adi and k_sifre:
              
              user = authenticate(request, username=k_adi, password=k_sifre)

              if user is not None:
                # useri login et
                login(request, user)
                # dashboarda gödner
                return redirect('home')
              
              else:
                #   böyle bir kullanıcı yok
                #  flash message ver
                return redirect('login')
         else:
             #  eksik bilgiler gönderildi
             return redirect('login')
                
    else:
        # get istekleri
        return render(request, 'login.html')


# user çıkış yaparsa
def cikis_yap(request):

    logout(request)
    return redirect('home')

def kayit_ol(request):

    # get ve post isteklerini ayikla
    if request.method == 'POST':
            # post isteklerinde veriyi işle
            print("sana gelen post:",request.POST)

            k_email = request.POST.get('k_email')
            k_adi = request.POST.get('k_adi')
            k_sifre = request.POST.get('k_sifre')

            if k_adi and k_email and k_sifre:
                
                # böyle bir user varmi?
                isRegistered = User.objects.filter(username = k_adi).first()

                if isRegistered:
                    # böyle bir user mevcut
                    # flash message
                    return redirect('register')
                
                # manager = objects
                User.objects.create_user(username = k_adi, email= k_email, password= k_sifre)
                # flash message geçebiliriz
                return redirect('login')
            else:
                # eksil bilgiler
                return redirect('register')
        
    else:
        # get istekleri için sayfayı render et
        return render(request, 'register.html')



# TWEETS ENDPOINT


# tweet detay
def tweetDetail(request, tweetId):
    context = {}

    validString = tweetId.isnumeric()

    if validString is False:
        return redirect('404')
    
    else:
        tweetId = int(tweetId)

    # bana gelen id'e göre bir veri var mı?
    tweet = Tweets.objects.filter(id=tweetId).first()

    if tweet:
        context['tweet'] = tweet

    else:
        # hata sayfası
        return redirect("404")
    

    return render(request, 'tweetDetail.html', context)


# tweet guncelle
def updateTweet(request, tweetId):

    tweet = Tweets.objects.filter(id = tweetId).first()

    if tweet is None:
        return redirect('404')
    
    if request.method == 'POST':
        
        form = CreateTweet(request.POST, instance=tweet)
        # eğer formda herhangi bir hata meydana gelmemişse
        if form.is_valid():

            form.save()
         
            # önceki url'i al. HTTP_REFERER bir önceki linki alir
            requestFrom = request.META['HTTP_REFERER']
            print("frommm:", requestFrom)

            # contains: eğer url /profil içeriyorsa
            if requestFrom.__contains__('/profil'):
                return redirect('user-profile', tweet.author.id)
            else:
                return redirect('tweet-detail', tweet.id)

        else:
            return redirect('home')


    else:
        return redirect('home')


# tweeti sil
def deleteTweet(request, tweetId):

    tweet = Tweets.objects.filter(id = tweetId).first()

    if tweet and tweet.author.id == request.user.id or request.user.is_superuser:
        # tweeti sil
        tweet.delete()
        return redirect("home")
    else:
        return redirect('404')
    

# profil alanı
def userProfile(request, userId):
    context = {}
    print("url:", request.path)
    # alternatif olarak request.user.id ile de çekebilirsin
    user = User.objects.filter(id = userId).first()

    if user:

        context['user'] = user

    else:
        return redirect('404')

    if request.method == 'POST':
            
  
        form = UpdateUser(request.POST, instance=user)

        name = request.POST.get('username')
        print("name:", name)
        print("username:", user.username)
        if name == user.username:

            messages.error(request, "Maalesef bu işlemi yapamıyoruz")
            return redirect('user-profile', user.id)

        if form.is_valid():
            # değişiklikleri veritabanına kaytitet
            form.save()

            messages.success(request, "Başarılı bir şekilde güncellendi")
            return redirect('user-profile', user.id)

        else:
            print("formdan gelen hatalar:", form.errors)
            messages.error(request, "Hata meydana geldi admine mail atınız")
            return redirect('user-profile', user.id)

    else:    
        context['userForm'] = UpdateUser(instance=user)
        # userin tweetlerini al
        # orm yapısında ilgili fieldin içine girebilmek için __ kullanılır
        # bu yapının ismi lookups dir.
        tweetedByUser = Tweets.objects.filter(author__id = user.id)
        context['userTweets'] = tweetedByUser

        updateForms = {}

        for twit in tweetedByUser:
            # instance = varolan modelin filedlerini miras alıp, formun içersine doldurmamızı sağlar
            updateForms[twit.id] = CreateTweet(instance=twit)

        # items key & value array şeklinde getirir
        context["updateForm"] = updateForms.items()

        # user banlı mı?
        isBanned = BannedUsers.objects.filter(suspect = user)

        if isBanned.count():
            context['records'] = { "banned": True, "record": isBanned.last(), "totalBans": isBanned.count() }

        # render et
        return render(request, 'profile.html', context)
    



# yorum yap
def createComment(request, tweetId):

    tweet = Tweets.objects.filter(id = tweetId).first()

    if tweet is None:
        return redirect('404')
    
    if request.method == 'POST':
        # django dosyaları request.FILES dan alır. request.FILES bir dict objesidir.
        # dosya = request.FILES.get('')
        form = CreateComment(request.POST, request.FILES)
        
        if form.is_valid():
        # form instancelerini oluştur ama henuz db'e kayit etme
           form = form.save(commit=False)
           form.author = request.user
           form.tweet = tweet
        #  artık kaydet
           form.save()
           return redirect("tweet-detail", tweet.id)
        
        else:
            return redirect('404')
        
    else:
        return redirect('home')


# yorım sil
def deleteComment(request, commentId):

    cacheTweetId = ""
    comment = TweetComments.objects.filter(id = commentId).first()

    if (comment):
        # tweetIdsini kurtar
        cacheTweetId = comment.tweet.id
        comment.delete()
        return redirect("tweet-detail", cacheTweetId)
    
    else:
        return redirect('404')

# yazarı banla
def banUser(request, userId):

    user = User.objects.filter(id = userId).first()

    if user is None:
            return redirect("404")
    
 
    if request.method == 'POST':
      
        reason = request.POST.get('reason')

        BannedUsers.objects.create(authorized = request.user, suspect = user, reason = reason)

        userTweets = Tweets.objects.filter(author=user)

        for tweet in userTweets:
            tweet.suspended = True
            tweet.save()

        
        return redirect("user-profile", user.id)

    else:

        return redirect('home')

# yazarın banını kaldır
def unbanUser(request, userId):
  

  user = User.objects.filter(id = userId).first()
  if user is None:
            return redirect("404")
    
    
  if request.method == 'POST':
        
        isBanned = BannedUsers.objects.filter(suspect = user).first()

        if isBanned:
            isBanned.delete()

        return redirect("user-profile", user.id)

  else:

        return redirect('home')





# API
def likeTweet(request, tweetId):
    response = {}

    if not request.user.is_authenticated:
        response['message'] = "User is not authenticated"
        return JsonResponse(response)
    # tweeti çek
    # TypeError: 'TweetLikes' instance expected, got <SimpleLazyObject: <User: admin2>>
    tweet = Tweets.objects.filter(id = tweetId).first()

    # isLiked = TweetLikes.objects.filter(user = request.user, tweet=tweet).first()
    isLiked = tweet.likes.filter(user = request.user, tweet = tweet).first()

    if (isLiked):
        # bu adamı bu listeden çıkart
        tweet.likes.remove(isLiked)
        # instanceyi sil
        isLiked.delete()
        # frontende actionu gönder
        response['action'] = "unlike"
    else:
        # post beğenildi
        # instance yarat
        liker = tweet.likes.create(user = request.user, tweet = tweet)
        # bu adamı bu postun likelerine ekle
        tweet.likes.add(liker)
        # frontende gönder
        response['action'] = "liked"

    # NOT: indexin render edildiği sayafa ufak bir konfigürasyon yapman gerekir.
    
    # beğeni sayısını gönder
    response['message'] = tweet.likes.count()
    return JsonResponse(response)