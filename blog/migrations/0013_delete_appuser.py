# Generated by Django 3.0.6 on 2020-05-25 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogConfig', '0012_appuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AppUser',
        ),
    ]
