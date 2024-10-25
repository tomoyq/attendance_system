import calendar
import datetime

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
        target_month = str(self.date.today.year) + ', ' + str(self.date.today.month)

        #今日の日付を渡したため今月のすべての日にちを持っているはず
        thisMonthDays = self.date.calculate_days(date = target_month)
        #タプルを要素にしたリストオブジェクトのため2つ目のindexで日付を調べる
        self.assertEqual(thisMonthDays[0][0], 1)

        #関数に１月１日のobjを渡すと１月のすべての日にちを持っているはず
        januaryDays = self.date.calculate_days(date='2024, 1')
        #monthrangeで月の日数を調べる(戻り値は(曜日の数字, 日数)のタプル)
        #januaryDaysの要素数が同じになるはず
        self.assertEqual(len(januaryDays), calendar.monthrange(2024, 1)[1])

    def test_calculate_five_months(self):
        month_list = self.date.calculate_five_month()

        #５つの要素を持っているはず
        self.assertEqual(len(month_list), 5)

        #１つ目の要素は今月を表すはず
        self.assertEqual(month_list[0], (self.date.today.year, self.date.today.month))
