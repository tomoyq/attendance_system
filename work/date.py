import calendar
import datetime

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
        #(年, 月, 日, 曜日)のリストを保持(nextで一つずつ取り出す)
        dates = self.itermonthdays4(target.year, target.month)

        #calendarには前月の最終日や次月の初日等不要な日付があるため
        #必要な日付だけのイテレータを作る
        dates_list = [i for i in dates if i[1] == target.month]
        
        return dates_list
        