# Generated by Django 5.1 on 2024-10-07 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0007_attendance_date_info_delete_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='info',
            options={'verbose_name': '勤怠情報', 'verbose_name_plural': '勤怠情報'},
        ),
    ]
