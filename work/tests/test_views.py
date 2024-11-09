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

class LoggedInEmployeeListViewTests(TestCase):
    def setUp(self):
        #管理者として２人登録する
        self.manager_tanaka = Manager.objects.create(name="田中太郎")
        self.manager_satou = Manager.objects.create(name="佐藤花子")
        #社員を１人, 管理者権限を持つ社員を２人登録する
        self.user_tanaka = CustomUser.objects.create_superuser(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager_tanaka)
        self.user_satou = CustomUser.objects.create_superuser(employee_number=222222, name="佐藤花子", password='test_pass' , manager_id=self.manager_satou)

        self.tanaka_deshi = CustomUser.objects.create(employee_number=121212, name="田中の弟子", password='test_pass' , manager_id=self.manager_tanaka)


    #getメソッドでアクセスするとステータスコードが200を返す
    #また、contextの中にログインしたuserのオブジェクトが入っている
    def test_get(self):
        #userにログインしておく
        self.client.force_login(self.user_tanaka)

        request = self.client.get(reverse('work:employeeList', kwargs={'managerId':self.user_tanaka.manager_id.pk}))
        self.assertEqual(request.status_code, 200)
        #templateはemployeeList.htmlを表示
        self.assertEqual(request.templates[0].name, 'work/employeeList.html')

        #requestの中のcontextにuserが入っているはず
        self.assertEqual(request.context['user'].name, self.user_tanaka.name)

    #クエリセットでログインしているuserが田中太郎の場合
    def test_query_set_by_user_tanaka(self):
        #userにログインしておく
        self.client.force_login(self.user_tanaka)

        request = self.client.get(reverse('work:employeeList', kwargs={'managerId':self.user_tanaka.manager_id.pk}))

        #user_tanakaが管理している社員は１人しかいないためquerysetの中は１つのはず
        self.assertEqual(len(request.context['object_list']), 1)

        #object_listの中には（田中の弟子）のデータしかないはず
        self.assertEqual(request.context['object_list'][0].name, self.tanaka_deshi.name)

    #クエリセットでログインしているuserが佐藤花子の場合
    def test_query_set_by_user_satou(self):
        #userにログインしておく
        self.client.force_login(self.user_satou)

        request = self.client.get(reverse('work:employeeList', kwargs={'managerId':self.user_satou.manager_id.pk}))

        #user_satouが管理している社員は１人もいないためquerysetの中は0のはず
        self.assertEqual(len(request.context['object_list']), 0)


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