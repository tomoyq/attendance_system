from django.test import TestCase
from django.urls import reverse, resolve

from acounts.models import CustomUser
from work.models import Manager

class UrlTest(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)
        #userにログインしておく
        self.client.force_login(self.user)
    
    #homeページのurlはhomeviewを表示しているか
    def test_home_url(self):
        #reverse関数は引数のurlを返す
        url = reverse('work:home', kwargs={'pk':self.user.employee_number})
        #resolve関数はurlから情報にアクセスできるようにresolvematchオブジェクトにする
        #view_nameはnamespaceとnameが:で結合されたものが入っている
        self.assertEqual(resolve(url).view_name, 'work:home')

    #employee_listページのurlはemployee_listviewを表示しているか
    def test_employee_list_url(self):
        #reverse関数は引数のurlを返す
        url = reverse('work:employeeList')
        #resolve関数はurlから情報にアクセスできるようにresolvematchオブジェクトにする
        #view_nameはnamespaceとnameが:で結合されたものが入っている
        self.assertEqual(resolve(url).view_name, 'work:employeeList')