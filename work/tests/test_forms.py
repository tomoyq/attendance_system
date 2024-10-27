import datetime

from django.test import TestCase
from acounts.models import CustomUser
from work.models import Attendance, Manager
from ..forms import EditForm

class TestEditForm(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager, )
        Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=datetime.datetime.now())
        
    #出勤時間がdatetime型ではない場合エラー
    def test_no_number(self):
        form_data = {
            "attendance_time" : '14:00',
        }
        form = EditForm(data=form_data)

        self.assertFalse(form.is_valid(), "出勤時間でエラーが出ませんでした。")