# Generated by Django 5.1 on 2024-10-07 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0003_alter_customuser_manager_id'),
        ('work', '0003_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('year', models.DateField(verbose_name='日付')),
                ('attendance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='work.attendance')),
            ],
        ),
    ]
