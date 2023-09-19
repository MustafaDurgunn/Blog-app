from django import forms


# tweet modelini al
from user_app.models import *

class CreateTweet(forms.ModelForm):

    class Meta:

        model = Tweets
        fields = ['tweet', 'image']



# yorum yapma modeli
class CreateComment(forms.ModelForm):

    class Meta:
        model = TweetComments
        fields = ['message', 'image']