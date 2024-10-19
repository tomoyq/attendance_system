from django.test import TestCase
from django.urls import reverse

from acounts.models import CustomUser
from work.models import Manager

class LoginViewTests(TestCase):
    
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        CustomUser.objects._create_user(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)
        self.data = [{"employee_number": "john", "password": "smith"},
                {"employee_number": 111111, "password": "test_pass",}]

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

    