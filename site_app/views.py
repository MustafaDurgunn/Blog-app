from django.shortcuts import render, redirect

# tweet model
from user_app.models import *

# form yapısını çağır
from .form import *

# dashboard
def index(request):
    # html de obje döndürmek icin olusturulur. 
    context = {}

    if request.method == 'POST':
        
        form = CreateTweet(request.POST)
        # bu if zorunludur
        # formda hicbir hata yoksa bu if ile verileri dbye kayıt et
        if form.is_valid():
       
            # veritabanına kayıt et
            form = form.save(commit=False)
            form.author = request.user
            # veritabanını kayıtet
            form.save()
            return redirect('tweet-detail', form.id)
        else:
            # formda 1 veya 1 den fazla hata meydana geldi
            print("[dashboard] form hataları:", form.errors)
            return redirect('home')

    else:
     
        # tüm tweetleri al
        allTweets = Tweets.objects.filter(suspended = False)
        updateForms = {}

        for twit in allTweets:
            # instance = varolan modelin filedlerini miras alıp, formun içersine doldurmamızı sağlar
            updateForms[twit.id] = CreateTweet(instance=twit)


 

        context['tweets'] = allTweets
   
        # tweet oluşturma formunu gönder
        context['tweetForm'] = CreateTweet()
        context['commentForm'] = CreateComment()
        context['updateForm'] = updateForms.items()

        if request.user.is_authenticated:
             # userin beğendi tweetleri bir array içinde gönder
            liked_tweets = list(Tweets.objects.filter(likes__user=request.user))
            context["liked_tweets"] = liked_tweets

        return render(request, 'index.html', context)


# 404 not found
def notFound(request):

    return render(request, "notFound.html")