# Generated by Django 3.0.6 on 2020-05-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogConfig', '0022_auto_20200526_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
