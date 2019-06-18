# Generated by Django 2.2.2 on 2019-06-18 08:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codebase',
            name='is_errors',
        ),
        migrations.RemoveField(
            model_name='codebase',
            name='processed_at',
        ),
        migrations.AddField(
            model_name='codebase',
            name='dependencies',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='requirements.txt'),
        ),
        migrations.AddField(
            model_name='codebase',
            name='interpreter',
            field=models.PositiveSmallIntegerField(choices=[(2, 'python'), (3, 'python3')], default=3, verbose_name='Python interpreter version'),
        ),
        migrations.AddField(
            model_name='codeexecution',
            name='has_errors',
            field=models.BooleanField(default=False, verbose_name='Does code have Errors?'),
        ),
        migrations.AddField(
            model_name='codeexecution',
            name='processed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Execution timestamp'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='codeexecution',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Code', to='mainapp.CodeBase'),
        ),
    ]
