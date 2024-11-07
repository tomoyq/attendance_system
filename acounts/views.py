from django.conf import settings

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, render

from .forms import AdminLoginForm, LoginForm

class LoginView(LoginView):
    def post(self, request, *args, **kwargs):
        #login_formからのpostリクエストの場合formにlogin_formを指定
        if 'login_form' in request.POST:
            login_form = LoginForm(data=request.POST)

            if login_form.is_valid():
                return self.form_valid(login_form=login_form)
            else:
                return self.form_invalid(login_form=login_form)
        #違う場合はadmin_login_formを指定
        else:
            admin_login_form = AdminLoginForm(data=request.POST)

            if admin_login_form.is_valid():
                return self.form_valid(admin_login_form=admin_login_form)
            else:
                return self.form_invalid(admin_login_form=admin_login_form)
            
    #バリデーションチェックが実行されたformごとにリダイレクト先を変更する
    def form_valid(self, login_form=None, admin_login_form=None):
        #login_formが渡された場合はsettingsのリダイレクト先に遷移させる
        if login_form is not None:
            auth_login(self.request, login_form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        
        #admin_login_formが渡された場合はリダイレクト先を社員一覧ページに変更する
        if admin_login_form is not None:
            auth_login(self.request, admin_login_form.get_user())
            return HttpResponseRedirect(self.get_admin_redirect_url())
        
            
    #それぞれのformのバリデーションに失敗した場合contextにエラーが出ているformを指定してエラーメッセージを表示
    def form_invalid(self, login_form=None, admin_login_form=None):
        #login_formが渡された場合contextのlogin_formにインスタンスを渡す
        if login_form is not None:
            context = {
                'login_form' : login_form,
                'admin_login_form' : AdminLoginForm()
            }
            return render(self.request, self.template_name, context)
        
        #admin_login_formが渡された場合はcontextのadmin_login_formにインスタンスを渡す
        if admin_login_form is not None:
            context = {
                'login_form' : LoginForm(),
                'admin_login_form' : admin_login_form,
                #再描画された時に管理者ログインのformを表示するためのフラグ
                'submit_form' : 'admin_login_form'
            }
            return render(self.request, self.template_name, context)

    def get_default_redirect_url(self):
        #リダイレクト先のurlにpkを渡す
        return resolve_url(settings.LOGIN_REDIRECT_URL, pk=int(self.request.user.pk))
    
    def get_admin_redirect_url(self):
        #リダイレクト先を社員一覧ページにする
        return resolve_url('work:employeeList', managerId=self.request.user.manager_id.pk)
    
    def get_context_data(self, **kwargs):
        #get_formを実行させないためformをnoneにする
        context =  super().get_context_data(form=None)
        context['login_form'] = LoginForm()
        context['admin_login_form'] = AdminLoginForm()

        return context
    