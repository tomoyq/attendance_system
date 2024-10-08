from django.db import models
from django.conf import settings


class Manager(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name= "名前"
    )

    #テーブルのレコード名
    def __str__(self):
        return self.name

    #テーブルの名前
    class Meta:
        verbose_name = "管理者"
        verbose_name_plural = "管理者"

class Attendance(models.Model):
    employee_number = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="社員番号",
        null=True,
    )
    date = models.DateField(
        verbose_name="出勤日",
        null=True,
    )
    attendance_time = models.TimeField(
        verbose_name="出勤時間"
    )
    closing_time = models.TimeField(
        verbose_name="退勤時間"
    )
    break_time = models.TimeField(
        verbose_name="休憩時間"
    )
    content = models.CharField(
        max_length=150,
        verbose_name="業務内容"
    )

    def __str__(self):
        return f'{str(self.employee_number.name)}さんの{str(self.date)}の勤怠状況'

    class Meta:
        verbose_name = "勤怠状況"
        verbose_name_plural = "勤怠状況"
        
        constraints = [
            #社員番号ー出勤日のペアでユニーク制約
            models.UniqueConstraint(
                fields=['employee_number', 'date'],
                name='employee_number_date_unique',
            ),
        ]
