# Generated by Django 2.2.4 on 2019-08-18 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_auto_20190817_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercode',
            old_name='code_id',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='usercode',
            old_name='user_id',
            new_name='user',
        ),
    ]
