# Generated by Django 3.0.6 on 2020-06-11 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogConfig', '0033_auto_20200611_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='slug',
        ),
    ]
