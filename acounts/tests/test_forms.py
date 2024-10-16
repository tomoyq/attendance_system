from django.test import TestCase
from acounts.models import CustomUser
from work.models import Manager
from ..forms import LoginForm

class Test_LoginForm(TestCase):

    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        #createメソッドだとパスワードがハッシュ化されないためis_validメソッドが常にfalseを返すため
        CustomUser.objects.create_user(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager, )

    #社員番号が数字ではない場合エラー
    def test_no_number(self):
        form_data = {
            "employee_number" : "社員番号",
            'password' : 'test_pass'
        }
        form = LoginForm(data=form_data)
        #form.is_valid()がTrueの時はログイン成功
        self.assertFalse(form.is_valid(), "社員番号でエラーが出ませんでした。")

    #社員番号の桁数が少ない場合エラー
    def test_different_digits(self):
        form_data = {
            "employee_number" : 11,
            'password' : 'test_pass'
        }
        form = LoginForm(data=form_data)
        #form.is_valid()がTrueの時はログイン成功
        self.assertFalse(form.is_valid(), "社員番号でエラーが出ませんでした。")

    #パスワードが違う場合エラー
    def test_different_passwaord(self):
        form_data = {
            "employee_number" : 111111,
            'password' : '222222'
        }
        form = LoginForm(data=form_data)
        #form.is_valid()がTrueの時はログイン成功
        self.assertFalse(form.is_valid(), "社員番号でエラーが出ませんでした。")

    #入力値が正しいとログインできる
    def test_login(self):
        form_data = {
            "employee_number" : 111111,
            "password" : 'test_pass'
        }
        form = LoginForm(data=form_data)
        #form.is_valid()がTrueの時はログイン成功
        self.assertTrue(form.is_valid(), form.errors)
