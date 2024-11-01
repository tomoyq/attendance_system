import calendar
import datetime
import locale

from django.test import TestCase

from work.date import CalculateDates

class CalculateDatesTest(TestCase):
    def setUp(self):
        self.date = CalculateDates()

    #コンストラクタのテスト
    def test_init(self):
        self.assertEqual(self.date.today, datetime.date.today())

    def test_caluculate_days(self):
        #formatが(年, 月)のためそれに合うように代入
        target_month = str(self.date.today.year) + str(self.date.today.month)

        #今日の日付を渡したため今月のすべての日にちを持っているはず
        thisMonthDays = self.date.calculate_days(date = target_month)
        #((年, 月), 日)のタプルを要素にしたリストオブジェクトのため2つ目のindexで日付を調べる
        self.assertEqual(thisMonthDays[1][0], 1)

        #関数に１月１日のobjを渡すと１月のすべての日にちを持っているはず
        januaryDays = self.date.calculate_days(date='20241')
        #monthrangeで月の日数を調べる(戻り値は(曜日の数字, 日数)のタプル)
        #januaryDaysの要素数が同じになるはず
        self.assertEqual(len(januaryDays[1]), calendar.monthrange(2024, 1)[1])

    def test_localize_date_list(self):
        #テストで使用するdate型のobj
        this_month_day = datetime.datetime(self.date.today.year, self.date.today.month, 1)
        january_day = datetime.datetime(2024, 1, 1)

        #formatが(年, 月)のためそれに合うように代入
        target_month = str(self.date.today.year) + str(self.date.today.month)

        #今日の日付を渡したため今月のすべての日にちを持っているはず
        thisMonthDays = self.date.localize_date_list(target_month = target_month)

        #関数に１月１日のobjを渡すと１月のすべての日にちを持っているはず
        januaryDays = self.date.localize_date_list(target_month='20241')

        self.assertEqual(len(thisMonthDays), calendar.monthrange(self.date.today.year, self.date.today.month)[1])
        self.assertEqual(len(januaryDays), calendar.monthrange(2024, 1)[1])

        #(日付, 曜日)のリストになっている
        self.assertEqual(thisMonthDays[0][1], this_month_day.strftime('%a'))
        self.assertEqual(januaryDays[0][1], january_day.strftime('%a'))

    def test_calculate_five_months(self):
        month_list = self.date.calculate_five_month()

        #５つの要素を持っているはず
        self.assertEqual(len(month_list), 5)

        #１つ目の要素は今月を表すはず
        self.assertEqual(month_list[0], (self.date.today.year, self.date.today.month))

    def test_change_datetime_from_post(self):
        target_month = f'{self.date.today.year} / {self.date.today.month}'

        target_obj = self.date.change_datetime_from_post(target=target_month, date='29日')

        #型はdateになっているはず
        self.assertTrue(isinstance(target_obj, datetime.date))
        self.assertEqual(target_obj, datetime.date(self.date.today.year, self.date.today.month, 29))
