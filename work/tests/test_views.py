from django.test import TestCase
from django.urls import reverse

from acounts.models import CustomUser
from work.models import Manager

class HomeViewTests(TestCase):
    
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)

    #getメソッドでアクセスするとステータスコードが200を返す
    def test_get(self):
        #userにログインしておく
        self.client.force_login(self.user)
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user.employee_number}))
        self.assertEqual(request.status_code, 200)
        #templatesはリスト形式でtemplate_nameを保持している
        #templateはhome.htmlを表示
        self.assertEqual(request.templates[0].name, 'work/home.html')

    #ログインしていないとログイン画面にリダイレクトする
    def test_not_login_user(self):
        target_url = reverse('work:home', kwargs={'pk':self.user.employee_number})
        login_url = reverse('acounts:login')
        #ログインしていない状態でhomeにアクセス
        request = self.client.get(target_url)
        #loginしていないためurlに?next=の文字がついているはず
        self.assertTrue(request.url, '{login_url}?next={target_url}'.format(login_url=login_url, target_url=target_url))

