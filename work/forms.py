from django import forms

from .models import Attendance

class EditForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['attendance_time', 'closing_time', 'break_time', 'content', ]


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
