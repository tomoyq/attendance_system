# Generated by Django 5.1 on 2024-10-08 09:10

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0005_alter_customuser_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='名前'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='employee_number',
            field=models.CharField(error_messages={'unique': 'A user with that employee_number already exists.'}, max_length=6, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9]{6}$')], verbose_name='社員番号'),
        ),
    ]