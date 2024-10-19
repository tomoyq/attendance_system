from django.test import TestCase
from django.urls import reverse, resolve


class UrlTest(TestCase):
    #loginページのurlはloginviewを表示しているか
    def test_login_url(self):
        #reverse関数は引数のurlを返す
        url = reverse('acounts:login')
        #resolve関数はurlから情報にアクセスできるようにresolvematchオブジェクトにする
        #view_nameはnamespaceとnameが:で結合されたものが入っている
        self.assertEqual(resolve(url).view_name, 'acounts:login')