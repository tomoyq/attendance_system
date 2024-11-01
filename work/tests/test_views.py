import datetime
import calendar

from django.test import TestCase
from django.urls import reverse

from acounts.models import CustomUser
from work.forms import EditForm
from work.models import Manager, Attendance
from work.views import HomeView

#loginしているときのテスト
class LoggedInHomeViewTests(TestCase):
    
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user_tanaka = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)
        self.user_satou = CustomUser.objects.create(employee_number=222222, name="佐藤花子", password='test_pass' , manager_id=self.manager)
        #userにログインしておく
        self.client.force_login(self.user_tanaka)

    #getメソッドでアクセスするとステータスコードが200を返す
    #また、contextの中にログインしたuserのオブジェクトが入っている
    def test_get(self):
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))
        self.assertEqual(request.status_code, 200)
        #templatesはリスト形式でtemplate_nameを保持している
        #templateはhome.htmlを表示
        self.assertEqual(request.templates[0].name, 'work/home.html')

        #requestの中のcontextにuserが入っているはず
        self.assertEqual(request.context['user'].name, self.user_tanaka.name)

    #ドロップダウンで何も選択していないときのdate_listは今月の日付をもっているはず
    def test_context_data_not_pulldown(self):
        today = datetime.date.today()
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))
        #今月の日数とdate_listの要素数が同じになるはず
        self.assertEqual(len(request.context['date_list']), calendar.monthrange(today.year, today.month)[1])

    #ドロップダウンで選択したときのdate_listは選択した月の日付をもっているはず
    def test_context_data_click_pulldown(self):
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}), data={'drop_down': '20241'})
        #drop_downで選択した月の日数とdate_listの要素数が同じになるはず
        self.assertEqual(len(request.context['date_list']), calendar.monthrange(2024, 1)[1])

    #クエリセットでログインしているuserのモデルをとれているか
    def test_query_set_user(self):
        Attendance.objects.create(employee_number=self.user_tanaka, date=datetime.date.today(), attendance_time=datetime.datetime.now())
        Attendance.objects.create(employee_number=self.user_satou, date=datetime.date.today(), attendance_time=datetime.datetime.now())

        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))

        #Attendanceにはuser_tanakaのデータは１つのため、object_listの中にもデータは1つしかないはず
        self.assertEqual(len(request.context['object_list']), 1)

        #object_listの中にはself.user_tanakaのデータしかないはず
        self.assertEqual(request.context['object_list'][0].employee_number.employee_number, str(self.user_tanaka.employee_number))

    #クエリセットで年月が同じものがとれているか
    def test_query_set_user(self):
        Attendance.objects.create(employee_number=self.user_tanaka, date=datetime.date.today(), attendance_time=datetime.datetime.now())
        Attendance.objects.create(employee_number=self.user_tanaka, date=datetime.datetime(2024, 1, 1), attendance_time=datetime.datetime.now())

        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))

        #Attendanceにはデータは2つある
        self.assertEqual(len(Attendance.objects.all()), 2)

        #object_listの中には今月のデータしかないはず
        self.assertEqual(len(request.context['object_list']), 1)

    #クエリセットで指定した月のデータがない場合フラグがtrueになるか
    def test_query_set_becomes_none(self):
        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))

        #Attendanceにはデータが一つもないため、object_listの中にもデータはないはず
        self.assertEqual(len(request.context['object_list']), 0)

        #is_querysetフラグがtrueになる
        self.assertEqual(request.context['is_queryset'], True)

    #日付だけのリストが入っているか
    def test_get_day_from_queyset(self):
        Attendance.objects.create(employee_number=self.user_tanaka, date=datetime.date.today(), attendance_time=datetime.datetime.now())

        request = self.client.get(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}))

        #querysetは１つのためqueryset_daysも１つである
        self.assertEqual(len(request.context['queryset_days']), 1)
        
        #querysetには今日の日付のデータが入っているためqueryset_daysにも今日の日付が入っている
        self.assertEqual(request.context['queryset_days'][0], datetime.date.today().day)

    #form_validメソッドを実行するとターゲットとなるモデルの値が更新される
    def test_form_valid(self):

        Attendance.objects.create(employee_number=self.user_tanaka, date=datetime.date.today(), attendance_time=datetime.datetime.now())

        instance = Attendance.objects.get(employee_number=self.user_tanaka, date=datetime.date.today(),)
        #まだ変更していないためcontentは空である
        self.assertEqual(instance.content, None)

        request = self.client.post(reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number}),
                                   data={'target-month':f'{datetime.date.today().year} / {datetime.date.today().month}',
                                         'target-obj':f'{datetime.date.today().day}日',
                                         "attendance_time" : '14:00',
                                         'closing_time' : '00:00',
                                         'break_time' : '01:00',
                                         'content' : '積み込み'},)
        
        instance = Attendance.objects.get(employee_number=self.user_tanaka, date=datetime.date.today(),)
        #form_validで保存されているためcontentに積み込みが入っているはず
        self.assertEqual(instance.content, '積み込み')



#ログインしていない場合のテスト
class NotLoginHomeViewTests(TestCase):

    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user_tanaka = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)

    #ログインしていないとログイン画面にリダイレクトする
    def test_not_login_user(self):
        target_url = reverse('work:home', kwargs={'pk':self.user_tanaka.employee_number})
        login_url = reverse('acounts:login')
        #ログインしていない状態でhomeにアクセス
        request = self.client.get(target_url)
        #loginしていないためurlに?next=の文字がついているはず
        self.assertTrue(request.url, '{login_url}?next={target_url}'.format(login_url=login_url, target_url=target_url))