import datetime

from django.test import TestCase
from acounts.models import CustomUser
from work.models import Attendance, Manager
from ..forms import EditForm

class TestInvalidEditForm(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager, )
        Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=datetime.datetime.now())
        
    #時間の入力フォーマットが違う場合のエラー
    def test_no_match_format_attendance_time(self):
        form_data = {
            #timeinputの入力形式が違う
            "attendance_time" : '1400',
        }
        form = EditForm(data=form_data)

        self.assertFalse(form.is_valid(), "出勤時間でエラーが出ませんでした。")
        #formのエラーの中にattendance_timeキーのものがあるかテスト
        self.assertIn('attendance_time', form.errors.keys())
        #attendance_timeフィールドのエラーメッセージが想定している物がでているか確認
        self.assertIn('HH:MM形式で入力して下さい。', form.errors['attendance_time'])

    def test_no_match_format_closing_time(self):
        form_data = {
            "attendance_time" : '14:00', 'closing_time' : '0000'
        }
        form = EditForm(data=form_data)

        self.assertFalse(form.is_valid(), "出勤時間でエラーが出ませんでした。")
        self.assertIn('closing_time', form.errors.keys())
        self.assertIn('HH:MM形式で入力して下さい。', form.errors['closing_time'])

    def test_no_match_format_break_time(self):
        form_data = {
            "attendance_time" : '14:00', 'closing_time' : '00:00', 'break_time' : '0000'
        }
        form = EditForm(data=form_data)

        self.assertFalse(form.is_valid(), "出勤時間でエラーが出ませんでした。")
        self.assertIn('break_time', form.errors.keys())
        self.assertIn('HH:MM形式で入力して下さい。', form.errors['break_time'])


class TestValidEditForm(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager, )
        Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=datetime.datetime.now())

    #formの値がバリデーションを通ったらis_validがtrueを返すか
    def test_is_valid_true(self):
        form_data = {
            "attendance_time" : '14:00', 'closing_time' : '00:00', 'break_time' : '01:00', 'content' : '積み込み'
        }
        form = EditForm(data=form_data)

        self.assertTrue(form.is_valid())
