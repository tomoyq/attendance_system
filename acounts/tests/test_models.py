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

    #社員番号は数字で6桁のものか
    def test_employee_number(self):
        user1 = CustomUser.objects.create(employee_number='1番', name="田中太郎", manager_id=self.manager, )
        #user2 = CustomUser.objects.create(employee_number='1111111', name="田中太郎", manager_id=self.manager, )
        with self.assertRaises(ValidationError):
            user1.full_clean()
        # with self.assertRaises(ValidationError):
        #     CustomUser.objects.create(employee_number='1番', name="田中太郎", manager_id=self.manager, )

    #社員番号はユニークであるか


    #名前とmanagerIDは必ず保持しているか