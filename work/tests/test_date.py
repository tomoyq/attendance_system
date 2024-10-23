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

        #関数に引数を渡してないため今月のすべての日にちを持っているはず
        thisMonthDays = self.date.calculate_days()
        #タプルを要素にしたリストオブジェクトのため2つ目のindexで月を調べる
        self.assertEqual(thisMonthDays[0][1], self.date.today.month)

        #関数に１月１日のobjを渡すと１月のすべての日にちを持っているはず
        januaryDays = self.date.calculate_days(date=datetime.date(2024, 1, 1))
        #2つ目のindexに１が入っているはず
        self.assertEqual(januaryDays[0][1], 1)
