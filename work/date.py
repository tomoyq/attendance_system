import calendar
import datetime

from dateutil.relativedelta import *

class CalculateDates(calendar.Calendar):

    firstweekday = 6

    #今日の日付を保持
    def __init__(self):
        self.today = datetime.date.today()

    #月の日数と曜日を取得
    def calculate_days(self, date=None):
        target = self.today
        if date:
            target = date

        #調べたい月を引数に渡す
        #(日, 曜日)のリストを保持(nextで一つずつ取り出す)
        dates = self.itermonthdays2(target.year, target.month)

        #calendarには前月の最終日や次月の初日等不要な日付がある(日付が0になっている)
        #必要な日付だけのイテレータを作る
        dates_list = [i for i in dates if i[0] != 0]
        
        return dates_list
    
    #当月から数えて五ヵ月分の月を取得
    def calculate_five_month(self):
        #リストに(年,月)のタプルを格納       
        lastFiveMonths = [((self.today - relativedelta(months=i)).year, (self.today - relativedelta(months=i)).month) 
                        for i in range(5)]
        return lastFiveMonths
        