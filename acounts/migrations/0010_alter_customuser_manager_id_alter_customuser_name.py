# Generated by Django 5.1 on 2024-10-11 10:04

import django.contrib.auth.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0009_alter_customuser_employee_number'),
        ('work', '0015_remove_date_attendance_remove_info_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='manager_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.manager'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='名前'),
        ),
    ]