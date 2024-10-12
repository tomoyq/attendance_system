from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import LoginForm

class LoginView(LoginView):
    form_class = LoginForm
    #ログイン済みの場合リダイレクト先に遷移させる
    redirect_authenticated_user = True
