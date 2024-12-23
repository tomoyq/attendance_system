from django.test import TestCase
from django.urls import reverse

from acounts.models import CustomUser
from work.models import Manager

class LoginViewLoginFormTests(TestCase):
    
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        CustomUser.objects._create_user(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)
        self.data = [{'login_form': 'true', "employee_number": "john", "password": "smith"},
                {'login_form': 'true', "employee_number": 111111, "password": "test_pass",}]

    #getメソッドでアクセスするとステータスコードが200を返す
    def test_get(self):
        request = self.client.get(reverse('acounts:login'))
        self.assertEqual(request.status_code, 200)

    #postメソッドでuserモデルと照合し見つからない場合status_codeは200を返すがtemplateはloginページのまま
    def test_error_post(self):
        request = self.client.post(reverse('acounts:login'), self.data[0])
        self.assertEqual(request.status_code, 200)
        #templatesはリスト形式でtemplate_nameを保持している
        self.assertEqual(request.templates[0].name, 'registration/login.html')

    #postメソッドでuserモデルと照合しログインに成功したらstatus_codeは最初302を返しそのあと200を返してリダイレクトする
    def test_success_post(self):
        request = self.client.post(reverse('acounts:login'), self.data[1])
        
        #status_code=はじめに返ってくるHTTPのレスポンスコード, target_status_code=最終的に返ってくるHTTPのレスポンスコード, msg_prefix=テスト結果のメッセージのプレフィックス,
        #fetch_redirect_response=最終ページをロードするか否か

        #self.data[1]の中のemployee_numberの値をurlのpkに渡す
        self.assertRedirects(request, reverse('work:home', kwargs={'pk':int(self.data[1]["employee_number"])}), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class LoginViewAdminLoginFormTests(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="管理者")
        CustomUser.objects._create_user(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)

        #管理者権限を持ったユーザーの作成
        self.admin = CustomUser.objects.create_superuser(employee_number=222222, name="管理者", password='test_pass' , manager_id=self.manager)

        #request.POSTの中にadmin_login_formを渡す
        self.data = [{'admin_login_form': 'true', "employee_number": 111111, "password": "test_pass"},
                {'admin_login_form': 'true', "employee_number": 222222, "password": "test_pass",}]
        
    #管理者ログインフォームから権限を持たないユーザーからのpostリクエスト
    def test_error_post(self):
        request = self.client.post(reverse('acounts:login'), self.data[0])
        self.assertEqual(request.status_code, 200)
        #templatesはリスト形式でtemplate_nameを保持している
        self.assertEqual(request.templates[0].name, 'registration/login.html')
        #contextの中に'submit_form'フラグが入っているはず
        self.assertIn('submit_form', request.context)

    #postメソッドでuserモデルと照合し管理者ログインに成功したらstatus_codeは最初302を返しそのあと200を返してリダイレクトする
    def test_success_post(self):
        request = self.client.post(reverse('acounts:login'), self.data[1])
        
        #status_code=はじめに返ってくるHTTPのレスポンスコード, target_status_code=最終的に返ってくるHTTPのレスポンスコード, msg_prefix=テスト結果のメッセージのプレフィックス,
        #fetch_redirect_response=最終ページをロードするか否か

        #リクエストの中のユーザーのmanaager_idをurlのmanagerIDに渡す
        self.assertRedirects(request, reverse('work:employeeList', kwargs={'managerId':self.admin.manager_id.pk}), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)