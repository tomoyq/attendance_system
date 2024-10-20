from django.test import TestCase
from django.urls import reverse, resolve

from acounts.models import CustomUser
from work.models import Manager

class UrlTest(TestCase):
    #loginページのurlはloginviewを表示しているか
    def test_login_url(self):
        #reverse関数は引数のurlを返す
        url = reverse('acounts:login')
        #resolve関数はurlから情報にアクセスできるようにresolvematchオブジェクトにする
        #view_nameはnamespaceとnameが:で結合されたものが入っている
        self.assertEqual(resolve(url).view_name, 'acounts:login')

    #logputページのurlに行くとログアウトするか
    def test_logout_url(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)
        #ログインしておく
        self.client.force_login(self.user)
        self.assertEqual(self.user.is_authenticated, True)

        #postメソッドでredirectを期待
        response = self.client.post(reverse('acounts:logout'))
        #リダイレクトするとstatus_codeは302を返す
        self.assertEqual(response.status_code, 302)
