# Generated by Django 2.2.4 on 2019-08-17 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_auto_20190807_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pywebuser',
            name='username',
            field=models.CharField(max_length=128, unique=True, verbose_name='username'),
        ),
    ]
