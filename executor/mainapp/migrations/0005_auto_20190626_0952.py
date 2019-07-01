# Generated by Django 2.2.2 on 2019-06-26 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20190619_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='codebase',
            name='hash_digest',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=128, null=True, verbose_name='SHA-512 digest of code text'),
        ),
        migrations.AlterField(
            model_name='codebase',
            name='dependencies',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='requirements.txt'),
        ),
    ]
