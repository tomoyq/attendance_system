from django.conf import settings

from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url

from .forms import LoginForm

class LoginView(LoginView):
    form_class = LoginForm
    #ログイン済みの場合リダイレクト先に遷移させる
    redirect_authenticated_user = True

    def get_default_url(self):
        #リダイレクト先のurlにpkを渡す
        return resolve_url(settings.LOGIN_REDIRECT_URL, pk=int(self.request.user.pk))