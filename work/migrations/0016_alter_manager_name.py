# Generated by Django 5.1 on 2024-10-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0015_remove_date_attendance_remove_info_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='名前'),
        ),
    ]
