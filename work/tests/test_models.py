import datetime

from django.db import IntegrityError

from django.test import TestCase
from acounts.models import CustomUser
from work.models import Manager, Attendance

class ManagerModelTest(TestCase):

    #初期状態では何も登録されていないことをチェック
    def test_is_empty(self):
        saved_manager = Manager.objects.all()
        self.assertEqual(saved_manager.count(), 0)

    #nameが空の場合エラー発生
    def test_empty_name(self):
        #null制約のエラーはintegrityerrorが発生
        with self.assertRaises(IntegrityError):
            Manager.objects.create(name=None)

    #nameはユニークであるか
    def test_unique_name(self):
        user1 = Manager.objects.create(name="田中太郎")
        user1.save()

        #既存のnameと重複するためエラー発生
        with self.assertRaises(IntegrityError):
            #unique_fieldのエラーはcreateメソッドの中のsaveメソッドの呼び出し時に発生
            Manager.objects.create(name="田中太郎")

class AttendanceModelTest(TestCase):
    def setUp(self):
        self.manager = Manager.objects.create(name="田中太郎")
        self.user = CustomUser.objects.create(employee_number=111111, name="田中太郎", password='test_pass' , manager_id=self.manager)

    #初期状態では何も登録されていないことをチェック
    def test_is_empty(self):
        saved_attendance = Attendance.objects.all()
        self.assertEqual(saved_attendance.count(), 0)

    #社員番号と日付はユニークか
    def test_employee_number_and_date(self):
        Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=datetime.datetime.today().time(),
        closing_time=None, break_time=None, content=None)

        with self.assertRaises(IntegrityError):
            #unique制約のエラーはcreateメソッドの中のsaveメソッドの呼び出し時に発生
            Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=datetime.datetime.today().time(),
            closing_time=None, break_time=None, content=None)


    #pkが空の場合エラー発生
    def test_empty_employee_number(self):
        #null制約のエラーはintegrityerrorが発生
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(employee_number=None, date=datetime.date.today(), attendance_time=datetime.datetime.today().time(),
            closing_time=None, break_time=None, content=None)

    def test_empty_date(self):
        #null制約のエラーはintegrityerrorが発生
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(employee_number=self.user, date=None, attendance_time=datetime.datetime.today().time(),
            closing_time=None, break_time=None, content=None)

    #出勤時間が空の場合エラー
    def test_empty_attendance_time(self):
        #null制約のエラーはintegrityerrorが発生
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(employee_number=self.user, date=datetime.date.today(), attendance_time=None,
            closing_time=None, break_time=None, content=None)

    #社員番号がusermodelに存在しない場合エラー
    def test_noMatch_employee_number(self):
        #foreignKeyのinstanseが見つからないエラーはvalueErrorが発生
        with self.assertRaises(ValueError):
            Attendance.objects.create(employee_number=222222, date=datetime.date.today(), attendance_time=datetime.datetime.today().time(),
            closing_time=None, break_time=None, content=None)