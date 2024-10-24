# Generated by Django 5.1 on 2024-10-21 09:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0011_alter_customuser_employee_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employee_number',
            field=models.IntegerField(error_messages={'unique': 'A user with that employee_number already exists.'}, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9]{6}$')], verbose_name='社員番号'),
        ),
    ]
