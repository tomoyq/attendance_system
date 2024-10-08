# Generated by Django 5.1 on 2024-10-07 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0011_info_attendance_remove_info_date_info_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='info',
            options={},
        ),
        migrations.RemoveField(
            model_name='info',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='info',
            name='date',
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, verbose_name='日付')),
                ('attendance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='work.attendance')),
            ],
            options={
                'verbose_name': '勤怠情報',
                'verbose_name_plural': '勤怠情報',
            },
        ),
        migrations.AddField(
            model_name='info',
            name='date',
            field=models.ManyToManyField(null=True, to='work.date'),
        ),
    ]
