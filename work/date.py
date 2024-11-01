import calendar
import datetime
import locale

from dateutil.relativedelta import *

class CalculateDates(calendar.Calendar):

    firstweekday = 6

    # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
    locale.setlocale(locale.LC_ALL, "")

    #今日の日付を保持
    def __init__(self):
        self.today = datetime.date.today()

    def change_str_datetime(self, date):
        #文字列型に変換したdateを(年, 月)のフォーマットでdate型に変換している
        return datetime.datetime.strptime(str(date), '%Y%m')

    #月の日数と曜日を取得
    def calculate_days(self, date):
        target = self.change_str_datetime(date=date)

        #調べたい月を引数に渡す
        #(日, 曜日)のリストを保持(nextで一つずつ取り出す)
        dates = self.itermonthdays(target.year, target.month)

        #calendarには前月の最終日や次月の初日等不要な日付がある(日付が0になっている)
        #必要な日付だけのイテレータを作る
        date_list = [i for i in dates if i != 0]
        
        return target, date_list
    
    #曜日を文字列の漢字に変える
    def localize_date_list(self, target_month):
        target, date_list = self.calculate_days(date=target_month)

        #(年-月-日)のdatetime型を要素に持つlistを作成
        datetime_obj =[datetime.date(target.year, target.month, date) for date in date_list]

        localize_date_list = []
        for date in datetime_obj:
            weekday = date.strftime('%a')
            localize_date_list.append((date.day, weekday))

        return localize_date_list
    
    #当月から数えて五ヵ月分の月を取得
    def calculate_five_month(self):
        #リストに(年,月)のタプルを格納       
        lastFiveMonths = [((self.today - relativedelta(months=i)).year, (self.today - relativedelta(months=i)).month) 
                        for i in range(5)]
        return lastFiveMonths
    
    #postメソッドで送られた値からdatetime型のobjを作成
    def change_datetime_from_post(self, target, date):
        #targetの中の空白文字でスライスして年と月をそれぞれ取得できるようにする
        sep = ' / '
        target = target.split(sep)
        #dateの中の'日'を削除して数字だけにする
        date = date.replace('日', '')

        return datetime.date(int(target[0]), int(target[1]), int(date))
