# Generated by Django 3.0.6 on 2020-05-29 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BlogConfig', '0025_auto_20200529_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='BlogConfig.AppUser'),
        ),
    ]
