# Generated by Django 5.1 on 2024-10-11 09:52

import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0006_remove_customuser_attendance_remove_customuser_id_and_more'),
        ('work', '0015_remove_date_attendance_remove_info_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employee_number',
            field=models.CharField(error_messages={'unique': 'A user with that employee_number already exists.'}, max_length=6, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='[0-9]{6}'), django.core.validators.MinLengthValidator(6)], verbose_name='社員番号'),
        ),
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
