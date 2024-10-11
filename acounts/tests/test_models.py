from django.db import IntegrityError
from django.core import checks

from django.core.exceptions import ValidationError
from django.test import TestCase
from acounts.models import CustomUser
from work.models import Manager

class CustomUserMmodelTest(TestCase):

    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")

    #初期状態では何も登録されていないことをチェック
    def test_is_empty(self):
        saved_user = CustomUser.objects.all()
        self.assertEqual(saved_user.count(), 0)

    #社員番号が数字で6桁未満の場合エラー発生するかチェック
    def test_employee_number(self):
        user1 = CustomUser.objects.create(employee_number=11, name="田中太郎", manager_id=self.manager, )
        
        #employee_numberが6桁未満のためエラー発生
        with self.assertRaises(ValidationError):
            #regexvalidatorのvalidationerror発生はcleanメソッドの後に発生する
            user1.full_clean()

    #社員番号はユニークであるか
    def test_unique_employee_number(self):
        user1 = CustomUser.objects.create(employee_number=111111, name="田中太郎", manager_id=self.manager, )
        user1.save()

        #既存のemployee_numberと重複するためエラー発生
        with self.assertRaises(IntegrityError):
            #unique_fieldのエラーはcreateメソッドの中のsaveメソッドの呼び出し時に発生
            CustomUser.objects.create(employee_number=111111, name="田中太郎", manager_id=self.manager, )

    #名前とmanagerIDは必ず保持しているか   
    def test_no_name(self):
        #名前がないためエラー発生
        with self.assertRaises(IntegrityError):
            #null制約のエラーはcreateメソッドの中のsaveメソッドの呼び出し時に発生
            CustomUser.objects.create(employee_number=111111, name=None, manager_id=self.manager, )

    def test_no_managerID(self):
        #managerIDがないためエラー発生
        with self.assertRaises(IntegrityError):
            #null制約のエラーはcreateメソッドの中のsaveメソッドの呼び出し時に発生
            CustomUser.objects.create(employee_number=111111, name="田中太郎", manager_id=None, )