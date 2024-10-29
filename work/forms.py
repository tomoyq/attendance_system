import datetime
import re

from django import forms

from .models import Attendance

def duration_format(duration):
    #秒からトータルの分数に変換
    total_minutes = int(duration.total_seconds() // 60)
    #トータルの分数を時間と分にそれぞれ分ける
    hour, minutes = divmod(total_minutes, 60)
    #:02dで秒数の欄に自動で0が入る
    return f'{hour}:{minutes:02d}'

class CustomDurationField(forms.DurationField):
    #フォームに表示するときのフォーマットを変更
    def prepare_value(self, value):
        #渡された値がdatetime.timedeltaであればduration_formatメソッドを実行
        if isinstance(value, datetime.timedelta):
            return duration_format(value)
        return value
    
    #入力された値を正しい形式に変換
    def to_python(self, value):
        if isinstance(value, str):
            #(時間):(分)の形式で入力されているか確認
            match = re.match(r'^(?P<hours>\d+):(?P<minutes>[0-5]?\d)$', value)
            if not match:
                raise forms.ValidationError('休憩時間は「時間:分」の形式で入力してください。')
            #matchメソッドでマッチした値は文字列で返るため整数型に変換
            hours = int(match.groups['hours'])
            minutes = int(match.groups['minutes'])
            return datetime.timedelta(hours=hours, minutes=minutes)
        
        return super().to_python(value)

class EditForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['attendance_time', 'closing_time', 'break_time', 'content', ]

        error_messages={
            'attendance_time': {
                'invalid': 'HH:MM形式で入力して下さい。'
            },
            'closing_time': {
                'invalid': 'HH:MM形式で入力して下さい。'
            },
        }

        attendance_time = forms.TimeInput(format='HH:MM')
        closing_time = forms.TimeInput(format='HH:MM')
        break_time = CustomDurationField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_classes = ('bg-gray-50 border border-gray-300 text-gray-900 rounded-lg mr-1 focus:ring-primary-600 focus:border-primary-600 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500')
        
        for field in self.fields.values():
            #classを追加
            field.widget.attrs['class'] = field_classes

        self.fields['attendance_time'].widget.attrs['id'] = 'modal-attendance'
        self.fields['closing_time'].widget.attrs['id'] = 'modal-closing'
        self.fields['break_time'].widget.attrs['id'] = 'modal-break'
        self.fields['content'].widget.attrs['id'] = 'modal-content'
        #contentフィールドだけw-2/4を追加したいためfield_classesを書き換え
        field_classes = ('w-2/4 bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500')
        self.fields['content'].widget.attrs['class'] = field_classes
