from django.shortcuts import render

# Create your views here.
from allauth.account.views import LogoutView
from oauth2_provider.models import AccessToken, RefreshToken

class CustomLogoutView(LogoutView):
    def logout(self):
        AccessToken.objects.filter(user=self.request.user).delete()
        RefreshToken.objects.filter(user=self.request.user).delete()
        super().logout()

