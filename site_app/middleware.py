from user_app.models import BannedUsers
from django.contrib.auth import logout

def isUserBanned(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
    
        if request.user.is_authenticated:

            isBanned = BannedUsers.objects.filter(suspect=request.user).last()

            if isBanned:
                logout(request)
            
        return response

    return middleware