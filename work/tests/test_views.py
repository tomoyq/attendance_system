import datetime
import calendar

from django.test import TestCase
from django.urls import reverse

from acounts.models import CustomUser
from work.models import Manager

class HomeViewTests(TestCase):
    
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)

    #ログインしていないとログイン画面にリダイレクトする
    def test_not_login_user(self):
        target_url = reverse('work:home', kwargs={'pk':self.user.employee_number})
        login_url = reverse('acounts:login')
        #ログインしていない状態でhomeにアクセス
        request = self.client.get(target_url)
        #loginしていないためurlに?next=の文字がついているはず
        self.assertTrue(request.url, '{login_url}?next={target_url}'.format(login_url=login_url, target_url=target_url))

    #getメソッドでアクセスするとステータスコードが200を返す
    #また、contextの中にログインしたuserのオブジェクトが入っている
    def test_get(self):
        #userにログインしておく
        self.client.force_login(self.user)
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user.employee_number}))
        self.assertEqual(request.status_code, 200)
        #templatesはリスト形式でtemplate_nameを保持している
        #templateはhome.htmlを表示
        self.assertEqual(request.templates[0].name, 'work/home.html')

        #requestの中のcontextにuserが入っているはず
        self.assertEqual(request.context['user'].name, self.user.name)

    #ドロップダウンで何も選択していないときのdate_listは今月の日付をもっているはず
    def test_context_data_not_pulldown(self):
        today = datetime.date.today()
        self.client.force_login(self.user)
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user.employee_number}))
        #今月の日数とdate_listの要素数が同じになるはず
        self.assertEqual(len(request.context['date_list']), calendar.monthrange(today.year, today.month)[1])

    #ドロップダウンで選択したときのdate_listは選択した月の日付をもっているはず
    def test_context_data_click_pulldown(self):
        self.client.force_login(self.user)
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user.employee_number}), data={'drop_down': '2024, 1'})
        #drop_downで選択した月の日数とdate_listの要素数が同じになるはず
        self.assertEqual(len(request.context['date_list']), calendar.monthrange(2024, 1)[1])