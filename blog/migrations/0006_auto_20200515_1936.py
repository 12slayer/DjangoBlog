# Generated by Django 3.0.6 on 2020-05-15 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogConfig', '0005_auto_20200515_1927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-publish_date', '-updated', '-timestamp']},
        ),
    ]
