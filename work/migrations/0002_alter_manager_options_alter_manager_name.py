# Generated by Django 5.1 on 2024-10-07 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manager',
            options={'verbose_name': '管理者', 'verbose_name_plural': '管理者'},
        ),
        migrations.AlterField(
            model_name='manager',
            name='name',
            field=models.CharField(max_length=150, verbose_name='名前'),
        ),
    ]
